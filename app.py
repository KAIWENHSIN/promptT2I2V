import React, { useState } from 'react';
import { Clapperboard, Sparkles, Wand2, Info, Languages, Globe } from 'lucide-react';
import Sidebar from './components/Sidebar';
import ResultCard from './components/ResultCard';
import { Settings, StylePreset, LensPreset, CameraAngle, CameraMovement, MovementDescriptions, PromptResult } from './types';
import { translateToEnglish, enhanceText } from './services/geminiService';

const App: React.FC = () => {
  const [subject, setSubject] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  
  const [settings, setSettings] = useState<Settings>({
    style: StylePreset.NatGeo,
    lens: LensPreset.Wide24mm,
    angle: CameraAngle.EyeLevel,
    movement: CameraMovement.Static,
  });
  
  const [results, setResults] = useState<PromptResult | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isEnhancingSubject, setIsEnhancingSubject] = useState(false);
  const [isEnhancingLocation, setIsEnhancingLocation] = useState(false);

  const handleEnhance = async (type: 'subject' | 'environment') => {
    const text = type === 'subject' ? subject : location;
    if (!text.trim()) return;

    if (type === 'subject') setIsEnhancingSubject(true);
    else setIsEnhancingLocation(true);

    try {
      const enhanced = await enhanceText(text, type);
      if (type === 'subject') setSubject(enhanced);
      else setLocation(enhanced);
    } catch (error) {
      console.error(`Enhance ${type} failed:`, error);
    } finally {
      if (type === 'subject') setIsEnhancingSubject(false);
      else setIsEnhancingLocation(false);
    }
  };

  const handleGenerate = async () => {
    if (!subject.trim()) return;
    setIsGenerating(true);

    try {
      // 1. Translate Inputs
      const [enSubject, enLocation] = await Promise.all([
        translateToEnglish(subject),
        location ? translateToEnglish(location) : Promise.resolve("Authentic lighting")
      ]);

      // Helper to strip Chinese translations from Enum values (e.g. "Wide (廣角)" -> "Wide")
      const getEnglish = (str: string) => str.split(' (')[0];

      // Negative prompt component
      const negPrompt = "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render";

      // 2. Construct Prompts
      // T2I: "RAW photo, {en_pt}. {camera_angle}, {lens_preset}. {en_kw}. {style_preset}, high-fidelity, documentary feel. --no ..."
      const t2i = `RAW photo, ${enLocation}. ${getEnglish(settings.angle)}, ${getEnglish(settings.lens)}. ${enSubject}. ${getEnglish(settings.style)}, high-fidelity, documentary feel. ${negPrompt}`;
      
      // I2V: "Mostly static camera with {move_desc}. [Subject: {en_kw} continues the same action]. ... --no ..."
      const moveDesc = MovementDescriptions[settings.movement];
      const i2v = `Mostly static camera with ${moveDesc}. [Subject: ${enSubject} continues the same action]. Realistic motion blur, no dramatic camera moves. ${negPrompt}`;

      setResults({ 
        t2i, 
        i2v, 
        translation: {
          subject: { original: subject, translated: enSubject },
          location: { original: location || "(Empty)", translated: enLocation }
        }
      });
    } catch (error) {
      console.error("Generation failed:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-gray-950 text-gray-100 font-sans">
      {/* Mobile Header */}
      <div className="md:hidden p-4 border-b border-gray-800 bg-gray-900 flex items-center gap-2">
        <Globe className="w-6 h-6 text-indigo-500" />
        <h1 className="text-lg font-bold">T2I2V Studio</h1>
      </div>

      {/* Sidebar */}
      <Sidebar settings={settings} setSettings={setSettings} />

      {/* Main Content */}
      <main className="flex-1 p-6 md:p-12 overflow-y-auto">
        <div className="max-w-5xl mx-auto space-y-8">
          
          {/* Header */}
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <span className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                 <Globe className="w-8 h-8" />
              </span>
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                雙語自動翻譯 T2I2V 工作站
              </h1>
            </div>
            <p className="text-gray-400 text-lg">
              輸入中文自動轉譯為英文 Prompt，支援全套實拍運鏡邏輯
            </p>
          </div>

          {/* Input Section */}
          <div className="bg-gray-900/50 rounded-2xl p-6 border border-gray-800 shadow-xl backdrop-blur-sm">
            <label className="flex items-center gap-2 text-sm font-medium text-gray-400 mb-4">
              <Languages className="w-4 h-4" />
              ✍️ 內容描述 (直接輸入中文)
            </label>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Subject Input */}
              <div className="space-y-2">
                <label className="text-xs text-gray-500 uppercase font-semibold tracking-wider">主體動作 / Subject</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="例如：貓咪在屋頂上曬太陽"
                    className="flex-1 bg-gray-950 border border-gray-700 text-white text-base rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 block p-4 placeholder-gray-600 transition-all"
                    onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                  />
                  <button
                    onClick={() => handleEnhance('subject')}
                    disabled={isEnhancingSubject || isGenerating || !subject}
                    className="flex items-center justify-center gap-2 px-4 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Enhance subject description with AI"
                  >
                    {isEnhancingSubject ? (
                      <Sparkles className="w-5 h-5 animate-spin" />
                    ) : (
                      <Sparkles className="w-5 h-5" />
                    )}
                    <span className="hidden sm:inline">Enhance</span>
                  </button>
                </div>
              </div>

              {/* Location Input */}
              <div className="space-y-2">
                <label className="text-xs text-gray-500 uppercase font-semibold tracking-wider">地點與光影 / Environment</label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="例如：地中海小島, 正午陽光"
                    className="flex-1 bg-gray-950 border border-gray-700 text-white text-base rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 block p-4 placeholder-gray-600 transition-all"
                    onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                  />
                  <button
                    onClick={() => handleEnhance('environment')}
                    disabled={isEnhancingLocation || isGenerating || !location}
                    className="flex items-center justify-center gap-2 px-4 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Enhance environment description with AI"
                  >
                    {isEnhancingLocation ? (
                      <Sparkles className="w-5 h-5 animate-spin" />
                    ) : (
                      <Sparkles className="w-5 h-5" />
                    )}
                    <span className="hidden sm:inline">Enhance</span>
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
               <button
                onClick={handleGenerate}
                disabled={isGenerating || !subject}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-900/20 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:hover:scale-100"
              >
                {isGenerating ? (
                  <Sparkles className="w-5 h-5 animate-spin" />
                ) : (
                  <Wand2 className="w-5 h-5" />
                )}
                {isGenerating ? 'Translating & Generating...' : '生成翻譯提示詞'}
              </button>
            </div>
          </div>

          {/* Results Section */}
          {results && (
            <div className="space-y-6 animate-fade-in">
              {/* Translation Check */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-900/30 border border-gray-800 rounded-lg p-4">
                   <h4 className="text-sm font-semibold text-gray-300 mb-1">📝 翻譯對照 (Keywords)</h4>
                   <p className="text-sm text-gray-500">CN: {results.translation.subject.original}</p>
                   <p className="text-sm text-indigo-400">EN: {results.translation.subject.translated}</p>
                </div>
                <div className="bg-gray-900/30 border border-gray-800 rounded-lg p-4">
                   <h4 className="text-sm font-semibold text-gray-300 mb-1">🌍 翻譯對照 (Environment)</h4>
                   <p className="text-sm text-gray-500">CN: {results.translation.location.original}</p>
                   <p className="text-sm text-indigo-400">EN: {results.translation.location.translated}</p>
                </div>
              </div>

              <div className="grid gap-6">
                <ResultCard
                  type="t2i"
                  title="Step 1: T2I (Kling/Midjourney) + Negative"
                  content={results.t2i}
                  description="Use this prompt to generate your base image first. Negative prompt is included."
                />
                
                <ResultCard
                  type="i2v"
                  title="Step 2: I2V (Runway/Kling) + Negative"
                  content={results.i2v}
                  description="Upload the generated image and use this for motion control. Negative prompt is included."
                />
              </div>

              <div className="flex items-start gap-3 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                <Info className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
                <p className="text-sm text-blue-300">
                  <strong>Pro Tip:</strong> For the best results in Runway Gen-3 or Kling's Image-to-Video mode, 
                  always upload the high-quality image generated from Step 1 as your reference. 
                  This ensures character consistency and visual fidelity.
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default App;
