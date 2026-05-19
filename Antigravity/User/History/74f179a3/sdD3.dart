import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_gemma/flutter_gemma.dart';
import '../models/vocab.dart';
import '../models/conversation.dart';

class ConversationService {
  static String _buildPrompt(List<N5Vocab> targetVocab) {
    final vocabStr = targetVocab.map((v) => '- ${v.kanji} (${v.hiragana}): ${v.english}').join('\n');
    return '''You are a JSON generator. Output ONLY valid JSON.
Write a natural, multi-line dialogue exchange (at least 3-4 lines total) appropriate for the JLPT N5 level.
CRITICAL RULE 1: You MUST include standard N5 Kanji in the Japanese text. Do not just use hiragana.
CRITICAL RULE 2: You MUST use the following vocabulary words in the conversation:
$vocabStr

Format exactly like this:
{"description":"...","lines":[{"speaker":"A","jp":"...","romaji":"...","en":"..."},{"speaker":"B","jp":"...","romaji":"...","en":"..."}]}

Do not add anything else. Stop immediately after the closing brace and output exactly: ###END###''';
  }

  static InferenceModel? _model;

  /// Pre-loads the model into memory in the background
  static Future<void> preLoadModel() async {
    try {
      final isInstalled = await FlutterGemma.hasActiveModel();
      if (isInstalled && _model == null) {
        debugPrint('🚀 Pre-loading AI model into memory...');
        _model = await FlutterGemma.getActiveModel(
          maxTokens: 350, // Reduced to force natural stop quickly for short Q&A
          // Removed preferredBackend: PreferredBackend.gpu to prevent native crashes on devices with low VRAM
        );
        debugPrint('✅ AI model loaded and ready!');
        
        // As soon as the model is loaded, quietly start generating the first conversation in the background!
        _startBackgroundGeneration();
      }
    } catch (e) {
      debugPrint('⚠️ Pre-loading failed: $e');
    }
  }

  static Future<Conversation>? _preGeneratedConv;
  static final ValueNotifier<String> backgroundStatus = ValueNotifier<String>('Idle');
  static bool _cancelRequested = false;
  static bool isGenerating = false;

  /// Starts a completely silent background generation
  static void _startBackgroundGeneration() {
    if (_preGeneratedConv != null) return; // Already generating or generated
    if (isGenerating) return; // Native model is busy!
    
    debugPrint('🔥 Kicking off background Pre-Generation to eliminate TTFT!');
    
    backgroundStatus.value = 'Starting background preparation...';
    _cancelRequested = false;
    _preGeneratedConv = _generateInternal(onProgress: (step) {
      backgroundStatus.value = step;
      debugPrint('Background Pre-Gen: $step');
    });
  }

  /// Public method to trigger background generation from the UI
  static void triggerBackgroundGeneration() {
    if (isGenerating) {
      debugPrint('⚠️ Ignored background trigger: Model is already busy generating!');
      return;
    }
    _preGeneratedConv = null; // Reset so a new one can start
    _startBackgroundGeneration();
  }

  /// Public method to manually stop any ongoing generation (foreground or background)
  static void cancelGeneration() {
    _cancelRequested = true;
    backgroundStatus.value = 'Idle';
    _preGeneratedConv = null;
    debugPrint('🛑 Generation cancelled by user.');
  }

  static Future<Conversation> generate({required Function(String) onProgress}) async {
    _cancelRequested = false;
    // If we already have a conversation cooking in the background, serve it instantly!
    if (_preGeneratedConv != null) {
      onProgress('Step 1/1: Retrieving pre-generated conversation... ⚡');
      debugPrint('⚡ Serving PRE-GENERATED conversation instantly!');
      
      try {
        final conv = await _preGeneratedConv!;
        _preGeneratedConv = null; // Consume it
        
        // Immediately start cooking the next one for the next time they click Generate!
        _startBackgroundGeneration();
        
        return conv;
      } catch (e) {
        debugPrint('⚠️ Background pre-gen failed, falling back to manual: $e');
        _preGeneratedConv = null;
      }
    }

    // Fallback if they click Generate before the background one finishes or if it failed
    debugPrint('🐢 Running manual generation (Pre-Gen was not ready)');
    final conv = await _generateInternal(onProgress: onProgress);
    
    // Start cooking the next one in the background
    _startBackgroundGeneration();
    return conv;
  }

  static Future<Conversation> _generateInternal({required Function(String) onProgress}) async {
    if (isGenerating) throw Exception('Generation already in progress!');
    isGenerating = true;
    
    try {
      onProgress('Step 1/6: Selecting vocabulary...');
      final targetVocab = N5Vocab.pickRandom(6);

      onProgress('Step 2/6: Building prompt for conversation...');
      final prompt = _buildPrompt(targetVocab);

      onProgress('Step 3/6: Initializing local AI model...');
        // Keep model in memory for much faster subsequent generations
        _model ??= await FlutterGemma.getActiveModel(
          maxTokens: 500, // Increased token limit to allow for longer 3-4 line conversations
          // Default backend is used here to prevent hard native crashes on devices with low VRAM
        );
        
        onProgress('Step 4/6: Creating inference session...');
        final session = await _model!.createSession(
          temperature: 0.1, // Low temperature for stable, deterministic JSON
          topK: 40,         // Avoid getting stuck in single-token loops
        );
        
        try {
          onProgress('Step 5/6: Sending prompt to AI...');
          await session.addQueryChunk(Message(text: prompt, isUser: true));
          
          onProgress('Step 6/6: Receiving response...\n\n');
          
          // Stream the response so the user can see exactly what the model outputs
          final stream = session.getResponseAsync();
          final buffer = StringBuffer();
          
          bool isStopping = false;
          await for (final chunk in stream) {
            if (_cancelRequested) {
              isStopping = true;
              session.stopGeneration();
              throw Exception('Generation stopped by user.');
            }
            
            if (isStopping) continue; // Ignore chunks while waiting for native side to stop

            buffer.write(chunk);
            final currentText = buffer.toString();
            
            // Show the raw output as it generates
            onProgress('Step 6/6: Receiving response...\n\n$currentText');
            
            // If we reach the end of the JSON
            if (currentText.contains('###END###') || currentText.contains('}```') || currentText.contains('}]}')) {
              isStopping = true;
              session.stopGeneration(); // Politely ask native engine to stop
              // CRITICAL: We DO NOT break here! 
              // We let the native engine finish its internal shutdown so the stream closes naturally.
              // This prevents the IllegalStateException when we call session.close() in the finally block.
            }
          }
          
          String response = buffer.toString().split('###END###').first.replaceAll(RegExp(r'<turn\|>.*'), '').trim();
        if (response.isEmpty) {
          throw Exception('Gemma returned an empty response.');
        }

        onProgress('Step 6/6: Parsing conversation...\n\n(This might take a moment, almost there!)');
        // Try to extract and parse JSON
        final parsed = _parseResponse(response);
        
        // Inject the target vocabulary into the conversation model!
        final finalConv = Conversation(
          description: parsed.description,
          vocabUsed: parsed.vocabUsed,
          lines: parsed.lines,
          questions: parsed.questions,
          targetVocab: targetVocab,
        );
        
        onProgress('Done! Loading UI...');
        return finalConv;
      } finally {
        // Close session but KEEP model loaded in RAM
        await session.close();
      }
    } finally {
      isGenerating = false;
    }
  }


  /// Attempt to parse the model's response, with repair strategies
  static Conversation _parseResponse(String raw) {
    // Strip markdown code fences if present
    String cleaned = raw
        .replaceAll(RegExp(r'```json\s*'), '')
        .replaceAll(RegExp(r'```\s*'), '')
        .trim();

    // Find the JSON object boundaries
    final start = cleaned.indexOf('{');
    final end = cleaned.lastIndexOf('}');
    if (start == -1 || end == -1) {
      throw Exception('No JSON object found in model response');
    }
    cleaned = cleaned.substring(start, end + 1);

    // Fix common issues from small models:
    // 1. Remove Japanese bracket artifacts 」「
    cleaned = cleaned.replaceAll('」「', '');
    cleaned = cleaned.replaceAll('」', '');
    cleaned = cleaned.replaceAll('「', '');

    // 2. Fix unescaped quotes inside strings (heuristic)
    // 3. Remove trailing commas before } or ]
    cleaned = cleaned.replaceAll(RegExp(r',\s*}'), '}');
    cleaned = cleaned.replaceAll(RegExp(r',\s*]'), ']');

    // Try parsing directly
    try {
      final json = jsonDecode(cleaned);
      return Conversation.fromJson(json);
    } catch (e) {
      // Third attempt: Fallback truncation safety net (user's safe_parse suggestion)
      final endTags = ['}]}', '}]', '}}', '}'];
      for (final endTag in endTags) {
        final idx = cleaned.lastIndexOf(endTag);
        if (idx != -1) {
          final candidate = cleaned.substring(0, idx + endTag.length);
          try {
            final json = jsonDecode(candidate);
            return Conversation.fromJson(json);
          } catch (_) {} // Keep trying other truncations
        }
      }
      
      // Final attempt: manual regex extraction
      return _buildFallbackConversation(cleaned);
    }
  }

  /// If JSON parsing totally fails, try to extract what we can
  static Conversation _buildFallbackConversation(String raw) {
    // Try to find and fix nested structure issues by balancing braces
    String attempt = _balanceBraces(raw);
    try {
      final json = jsonDecode(attempt);
      return Conversation.fromJson(json);
    } catch (_) {}

    // Last resort: try extracting lines manually from partial JSON
    final lines = <ConversationLine>[];
    final linePattern = RegExp(
      r'"speaker"\s*:\s*"([AB])"\s*,\s*"name"\s*:\s*"([^"]*?)"\s*,\s*"jp"\s*:\s*"([^"]*?)"\s*,\s*"romaji"\s*:\s*"([^"]*?)"\s*,\s*"en"\s*:\s*"([^"]*?)"',
    );

    for (final match in linePattern.allMatches(raw)) {
      lines.add(ConversationLine(
        speaker: match.group(1) ?? 'A',
        name: match.group(2) ?? '',
        jp: match.group(3) ?? '',
        romaji: match.group(4) ?? '',
        en: match.group(5) ?? '',
      ));
    }

    if (lines.isEmpty) {
      throw Exception('Could not parse model response into a conversation. The model may need to be upgraded to gemma3:4b for better JSON output.');
    }

    // Extract description if possible
    final descMatch = RegExp(r'"description"\s*:\s*"([^"]*?)"').firstMatch(raw);

    return Conversation(
      description: descMatch?.group(1) ?? 'N5 Conversation',
      vocabUsed: [],
      lines: lines,
      questions: [],
    );
  }

  /// Try to fix unbalanced braces/brackets
  static String _balanceBraces(String json) {
    int braces = 0;
    int brackets = 0;
    final buf = StringBuffer();

    for (int i = 0; i < json.length; i++) {
      final c = json[i];
      if (c == '{') braces++;
      if (c == '}') braces--;
      if (c == '[') brackets++;
      if (c == ']') brackets--;
      buf.write(c);

      // If we've closed the root object, stop
      if (braces == 0 && i > 0) break;
    }

    // Close any unclosed brackets/braces
    while (brackets > 0) {
      buf.write(']');
      brackets--;
    }
    while (braces > 0) {
      buf.write('}');
      braces--;
    }

    return buf.toString();
  }
}
