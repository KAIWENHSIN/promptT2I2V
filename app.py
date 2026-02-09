{\rtf1\ansi\ansicpg950\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;\f1\fnil\fcharset136 PingFangTC-Regular;\f2\fnil\fcharset0 AppleColorEmoji;
}
{\colortbl;\red255\green255\blue255;\red70\green137\blue204;\red24\green24\blue24;\red202\green202\blue202;
\red54\green192\blue160;\red212\green212\blue212;\red194\green126\blue101;\red79\green123\blue61;\red167\green197\blue152;
\red238\green46\blue56;}
{\*\expandedcolortbl;;\cssrgb\c33725\c61176\c83922;\cssrgb\c12157\c12157\c12157;\cssrgb\c83137\c83137\c83137;
\cssrgb\c23922\c78824\c69020;\cssrgb\c86275\c86275\c86275;\cssrgb\c80784\c56863\c47059;\cssrgb\c37647\c54510\c30588;\cssrgb\c70980\c80784\c65882;
\cssrgb\c95686\c27843\c27843;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
import\cf4  \cf5 React\cf6 ,\cf4  \cf6 \{\cf4  useState \cf6 \}\cf4  \cf2 from\cf4  \cf7 'react'\cf6 ;\cf4 \cb1 \
\cf2 \cb3 import\cf4  \cf6 \{\cf4  \cf5 Clapperboard\cf6 ,\cf4  \cf5 Sparkles\cf6 ,\cf4  \cf5 Wand2\cf6 ,\cf4  \cf5 Info\cf6 ,\cf4  \cf5 Languages\cf6 ,\cf4  \cf5 Globe\cf4  \cf6 \}\cf4  \cf2 from\cf4  \cf7 'lucide-react'\cf6 ;\cf4 \cb1 \
\cf2 \cb3 import\cf4  \cf5 Sidebar\cf4  \cf2 from\cf4  \cf7 './components/Sidebar'\cf6 ;\cf4 \cb1 \
\cf2 \cb3 import\cf4  \cf5 ResultCard\cf4  \cf2 from\cf4  \cf7 './components/ResultCard'\cf6 ;\cf4 \cb1 \
\cf2 \cb3 import\cf4  \cf6 \{\cf4  \cf5 Settings\cf6 ,\cf4  \cf5 StylePreset\cf6 ,\cf4  \cf5 LensPreset\cf6 ,\cf4  \cf5 CameraAngle\cf6 ,\cf4  \cf5 CameraMovement\cf6 ,\cf4  \cf5 MovementDescriptions\cf6 ,\cf4  \cf5 PromptResult\cf4  \cf6 \}\cf4  \cf2 from\cf4  \cf7 './types'\cf6 ;\cf4 \cb1 \
\cf2 \cb3 import\cf4  \cf6 \{\cf4  translateToEnglish\cf6 ,\cf4  enhanceText \cf6 \}\cf4  \cf2 from\cf4  \cf7 './services/geminiService'\cf6 ;\cf4 \cb1 \
\
\cf2 \cb3 const\cf4  \cf5 App\cf6 :\cf4  \cf5 React\cf6 .\cf5 FC\cf4  \cf6 =\cf4  \cf6 ()\cf4  \cf6 =>\cf4  \cf6 \{\cf4 \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 subject\cf6 ,\cf4  setSubject\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 <\cf2 string\cf6 >(\cf7 ''\cf6 );\cf4 \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 location\cf6 ,\cf4  setLocation\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 <\cf2 string\cf6 >(\cf7 ''\cf6 );\cf4 \cb1 \
\cb3   \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 settings\cf6 ,\cf4  setSettings\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 <\cf5 Settings\cf6 >(\{\cf4 \cb1 \
\cb3     style\cf6 :\cf4  \cf5 StylePreset\cf6 .\cf5 NatGeo\cf6 ,\cf4 \cb1 \
\cb3     lens\cf6 :\cf4  \cf5 LensPreset\cf6 .\cf5 Wide24mm\cf6 ,\cf4 \cb1 \
\cb3     angle\cf6 :\cf4  \cf5 CameraAngle\cf6 .\cf5 EyeLevel\cf6 ,\cf4 \cb1 \
\cb3     movement\cf6 :\cf4  \cf5 CameraMovement\cf6 .\cf5 Static\cf6 ,\cf4 \cb1 \
\cb3   \cf6 \});\cf4 \cb1 \
\cb3   \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 results\cf6 ,\cf4  setResults\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 <\cf5 PromptResult\cf4  \cf6 |\cf4  \cf2 null\cf6 >(\cf2 null\cf6 );\cf4 \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 isGenerating\cf6 ,\cf4  setIsGenerating\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 isEnhancingSubject\cf6 ,\cf4  setIsEnhancingSubject\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\cb3   \cf2 const\cf4  \cf6 [\cf4 isEnhancingLocation\cf6 ,\cf4  setIsEnhancingLocation\cf6 ]\cf4  \cf6 =\cf4  useState\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\
\cb3   \cf2 const\cf4  handleEnhance \cf6 =\cf4  \cf2 async\cf4  \cf6 (\cf2 type\cf6 :\cf4  \cf7 'subject'\cf4  \cf6 |\cf4  \cf7 'environment'\cf6 )\cf4  \cf6 =>\cf4  \cf6 \{\cf4 \cb1 \
\cb3     \cf2 const\cf4  text \cf6 =\cf4  \cf2 type\cf4  \cf6 ===\cf4  \cf7 'subject'\cf4  \cf6 ?\cf4  subject \cf6 :\cf4  location\cf6 ;\cf4 \cb1 \
\cb3     \cf2 if\cf4  \cf6 (!\cf4 text\cf6 .\cf4 trim\cf6 ())\cf4  \cf2 return\cf6 ;\cf4 \cb1 \
\
\cb3     \cf2 if\cf4  \cf6 (\cf2 type\cf4  \cf6 ===\cf4  \cf7 'subject'\cf6 )\cf4  setIsEnhancingSubject\cf6 (\cf2 true\cf6 );\cf4 \cb1 \
\cb3     \cf2 else\cf4  setIsEnhancingLocation\cf6 (\cf2 true\cf6 );\cf4 \cb1 \
\
\cb3     \cf2 try\cf4  \cf6 \{\cf4 \cb1 \
\cb3       \cf2 const\cf4  enhanced \cf6 =\cf4  \cf2 await\cf4  enhanceText\cf6 (\cf4 text\cf6 ,\cf4  \cf2 type\cf6 );\cf4 \cb1 \
\cb3       \cf2 if\cf4  \cf6 (\cf2 type\cf4  \cf6 ===\cf4  \cf7 'subject'\cf6 )\cf4  setSubject\cf6 (\cf4 enhanced\cf6 );\cf4 \cb1 \
\cb3       \cf2 else\cf4  setLocation\cf6 (\cf4 enhanced\cf6 );\cf4 \cb1 \
\cb3     \cf6 \}\cf4  \cf2 catch\cf4  \cf6 (\cf4 error\cf6 )\cf4  \cf6 \{\cf4 \cb1 \
\cb3       console\cf6 .\cf4 error\cf6 (\cf7 `Enhance \cf6 $\{\cf2 type\cf6 \}\cf7  failed:`\cf6 ,\cf4  error\cf6 );\cf4 \cb1 \
\cb3     \cf6 \}\cf4  \cf2 finally\cf4  \cf6 \{\cf4 \cb1 \
\cb3       \cf2 if\cf4  \cf6 (\cf2 type\cf4  \cf6 ===\cf4  \cf7 'subject'\cf6 )\cf4  setIsEnhancingSubject\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\cb3       \cf2 else\cf4  setIsEnhancingLocation\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\cb3     \cf6 \}\cf4 \cb1 \
\cb3   \cf6 \};\cf4 \cb1 \
\
\cb3   \cf2 const\cf4  handleGenerate \cf6 =\cf4  \cf2 async\cf4  \cf6 ()\cf4  \cf6 =>\cf4  \cf6 \{\cf4 \cb1 \
\cb3     \cf2 if\cf4  \cf6 (!\cf4 subject\cf6 .\cf4 trim\cf6 ())\cf4  \cf2 return\cf6 ;\cf4 \cb1 \
\cb3     setIsGenerating\cf6 (\cf2 true\cf6 );\cf4 \cb1 \
\
\cb3     \cf2 try\cf4  \cf6 \{\cf4 \cb1 \
\cb3       \cf8 // 1. Translate Inputs\cf4 \cb1 \
\cb3       \cf2 const\cf4  \cf6 [\cf4 enSubject\cf6 ,\cf4  enLocation\cf6 ]\cf4  \cf6 =\cf4  \cf2 await\cf4  \cf5 Promise\cf6 .\cf4 all\cf6 ([\cf4 \cb1 \
\cb3         translateToEnglish\cf6 (\cf4 subject\cf6 ),\cf4 \cb1 \
\cb3         location \cf6 ?\cf4  translateToEnglish\cf6 (\cf4 location\cf6 )\cf4  \cf6 :\cf4  \cf5 Promise\cf6 .\cf4 resolve\cf6 (\cf7 "Authentic lighting"\cf6 )\cf4 \cb1 \
\cb3       \cf6 ]);\cf4 \cb1 \
\
\cb3       \cf8 // Helper to strip Chinese translations from Enum values (e.g. "Wide (
\f1 \'bc\'73\'a8\'a4
\f0 )" -> "Wide")\cf4 \cb1 \
\cb3       \cf2 const\cf4  getEnglish \cf6 =\cf4  \cf6 (\cf4 str\cf6 :\cf4  \cf2 string\cf6 )\cf4  \cf6 =>\cf4  str\cf6 .\cf4 split\cf6 (\cf7 ' ('\cf6 )[\cf9 0\cf6 ];\cf4 \cb1 \
\
\cb3       \cf8 // Negative prompt component\cf4 \cb1 \
\cb3       \cf2 const\cf4  negPrompt \cf6 =\cf4  \cf7 "--no flicker, no warping, no melting, no jitter, no text, no watermark, animation, cgi, 3d render"\cf6 ;\cf4 \cb1 \
\
\cb3       \cf8 // 2. Construct Prompts\cf4 \cb1 \
\cb3       \cf8 // T2I: "RAW photo, \{en_pt\}. \{camera_angle\}, \{lens_preset\}. \{en_kw\}. \{style_preset\}, high-fidelity, documentary feel. --no ..."\cf4 \cb1 \
\cb3       \cf2 const\cf4  t2i \cf6 =\cf4  \cf7 `RAW photo, \cf6 $\{\cf4 enLocation\cf6 \}\cf7 . \cf6 $\{\cf4 getEnglish\cf6 (\cf4 settings\cf6 .\cf4 angle\cf6 )\}\cf7 , \cf6 $\{\cf4 getEnglish\cf6 (\cf4 settings\cf6 .\cf4 lens\cf6 )\}\cf7 . \cf6 $\{\cf4 enSubject\cf6 \}\cf7 . \cf6 $\{\cf4 getEnglish\cf6 (\cf4 settings\cf6 .\cf4 style\cf6 )\}\cf7 , high-fidelity, documentary feel. \cf6 $\{\cf4 negPrompt\cf6 \}\cf7 `\cf6 ;\cf4 \cb1 \
\cb3       \cb1 \
\cb3       \cf8 // I2V: "Mostly static camera with \{move_desc\}. [Subject: \{en_kw\} continues the same action]. ... --no ..."\cf4 \cb1 \
\cb3       \cf2 const\cf4  moveDesc \cf6 =\cf4  \cf5 MovementDescriptions\cf6 [\cf4 settings\cf6 .\cf4 movement\cf6 ];\cf4 \cb1 \
\cb3       \cf2 const\cf4  i2v \cf6 =\cf4  \cf7 `Mostly static camera with \cf6 $\{\cf4 moveDesc\cf6 \}\cf7 . [Subject: \cf6 $\{\cf4 enSubject\cf6 \}\cf7  continues the same action]. Realistic motion blur, no dramatic camera moves. \cf6 $\{\cf4 negPrompt\cf6 \}\cf7 `\cf6 ;\cf4 \cb1 \
\
\cb3       setResults\cf6 (\{\cf4  \cb1 \
\cb3         t2i\cf6 ,\cf4  \cb1 \
\cb3         i2v\cf6 ,\cf4  \cb1 \
\cb3         translation\cf6 :\cf4  \cf6 \{\cf4 \cb1 \
\cb3           subject\cf6 :\cf4  \cf6 \{\cf4  original\cf6 :\cf4  subject\cf6 ,\cf4  translated\cf6 :\cf4  enSubject \cf6 \},\cf4 \cb1 \
\cb3           location\cf6 :\cf4  \cf6 \{\cf4  original\cf6 :\cf4  location \cf6 ||\cf4  \cf7 "(Empty)"\cf6 ,\cf4  translated\cf6 :\cf4  enLocation \cf6 \}\cf4 \cb1 \
\cb3         \cf6 \}\cf4 \cb1 \
\cb3       \cf6 \});\cf4 \cb1 \
\cb3     \cf6 \}\cf4  \cf2 catch\cf4  \cf6 (\cf4 error\cf6 )\cf4  \cf6 \{\cf4 \cb1 \
\cb3       console\cf6 .\cf4 error\cf6 (\cf7 "Generation failed:"\cf6 ,\cf4  error\cf6 );\cf4 \cb1 \
\cb3     \cf6 \}\cf4  \cf2 finally\cf4  \cf6 \{\cf4 \cb1 \
\cb3       setIsGenerating\cf6 (\cf2 false\cf6 );\cf4 \cb1 \
\cb3     \cf6 \}\cf4 \cb1 \
\cb3   \cf6 \};\cf4 \cb1 \
\
\cb3   \cf2 return\cf4  \cf6 (\cf4 \cb1 \
\cb3     \cf6 <\cf4 div className\cf6 =\cf7 "flex flex-col md:flex-row min-h-screen bg-gray-950 text-gray-100 font-sans"\cf6 >\cf4 \cb1 \
\cb3       \cf6 \{\cf8 /* Mobile Header */\cf6 \}\cf4 \cb1 \
\cb3       \cf6 <\cf4 div className\cf6 =\cf7 "md:hidden p-4 border-b border-gray-800 bg-gray-900 flex items-center gap-2"\cf6 >\cf4 \cb1 \
\cb3         \cf6 <\cf5 Globe\cf4  className\cf6 =\cf7 "w-6 h-6 text-indigo-500"\cf4  />\cb1 \
\cb3         \cf6 <\cf4 h1 className\cf6 =\cf7 "text-lg font-bold"\cf6 >\cf5 T2I2V\cf4  \cf5 Studio\cf6 </\cf4 h1\cf6 >\cf4 \cb1 \
\cb3       \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3       \cf6 \{\cf8 /* Sidebar */\cf6 \}\cf4 \cb1 \
\cb3       \cf6 <\cf5 Sidebar\cf4  settings\cf6 =\{\cf4 settings\cf6 \}\cf4  setSettings\cf6 =\{\cf4 setSettings\cf6 \}\cf4  />\cb1 \
\
\cb3       \cf6 \{\cf8 /* Main Content */\cf6 \}\cf4 \cb1 \
\cb3       \cf6 <\cf4 main className\cf6 =\cf7 "flex-1 p-6 md:p-12 overflow-y-auto"\cf6 >\cf4 \cb1 \
\cb3         \cf6 <\cf4 div className\cf6 =\cf7 "max-w-5xl mx-auto space-y-8"\cf6 >\cf4 \cb1 \
\cb3           \cb1 \
\cb3           \cf6 \{\cf8 /* Header */\cf6 \}\cf4 \cb1 \
\cb3           \cf6 <\cf4 div className\cf6 =\cf7 "space-y-2"\cf6 >\cf4 \cb1 \
\cb3             \cf6 <\cf4 div className\cf6 =\cf7 "flex items-center gap-3"\cf6 >\cf4 \cb1 \
\cb3               \cf6 <\cf4 span className\cf6 =\cf7 "p-2 rounded-lg bg-indigo-500/10 text-indigo-400"\cf6 >\cf4 \cb1 \
\cb3                  \cf6 <\cf5 Globe\cf4  className\cf6 =\cf7 "w-8 h-8"\cf4  />\cb1 \
\cb3               \cf6 </\cf4 span\cf6 >\cf4 \cb1 \
\cb3               \cf6 <\cf4 h1 className\cf6 =\cf7 "text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent"\cf6 >\cf4 \cb1 \
\cb3                 
\f1 \cf10 \'c2\'f9\'bb\'79\'a6\'db\'b0\'ca\'c2\'bd\'c4\'b6
\f0 \cf4  \cf5 T2I2V\cf4  
\f1 \cf10 \'a4\'75\'a7\'40\'af\'b8
\f0 \cf4 \cb1 \
\cb3               \cf6 </\cf4 h1\cf6 >\cf4 \cb1 \
\cb3             \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3             \cf6 <\cf4 p className\cf6 =\cf7 "text-gray-400 text-lg"\cf6 >\cf4 \cb1 \
\cb3               
\f1 \cf10 \'bf\'e9\'a4\'4a\'a4\'a4\'a4\'e5\'a6\'db\'b0\'ca\'c2\'e0\'c4\'b6\'ac\'b0\'ad\'5e\'a4\'e5
\f0 \cf4  \cf5 Prompt
\f1 \cf10 \'a1\'41\'a4\'e4\'b4\'a9\'a5\'fe\'ae\'4d\'b9\'ea\'a9\'e7\'b9\'42\'c3\'e8\'c5\'de\'bf\'e8
\f0 \cf4 \cb1 \
\cb3             \cf6 </\cf4 p\cf6 >\cf4 \cb1 \
\cb3           \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3           \cf6 \{\cf8 /* Input Section */\cf6 \}\cf4 \cb1 \
\cb3           \cf6 <\cf4 div className\cf6 =\cf7 "bg-gray-900/50 rounded-2xl p-6 border border-gray-800 shadow-xl backdrop-blur-sm"\cf6 >\cf4 \cb1 \
\cb3             \cf6 <\cf4 label className\cf6 =\cf7 "flex items-center gap-2 text-sm font-medium text-gray-400 mb-4"\cf6 >\cf4 \cb1 \
\cb3               \cf6 <\cf5 Languages\cf4  className\cf6 =\cf7 "w-4 h-4"\cf4  />\cb1 \
\cb3               
\f2 \cf10 \uc0\u9997 \u65039 
\f0 \cf4  
\f1 \cf10 \'a4\'ba\'ae\'65\'b4\'79\'ad\'7a
\f0 \cf4  \cf6 (
\f1 \cf10 \'aa\'bd\'b1\'b5\'bf\'e9\'a4\'4a\'a4\'a4\'a4\'e5
\f0 \cf6 )\cf4 \cb1 \
\cb3             \cf6 </\cf4 label\cf6 >\cf4 \cb1 \
\cb3             \cb1 \
\cb3             \cf6 <\cf4 div className\cf6 =\cf7 "grid grid-cols-1 md:grid-cols-2 gap-4"\cf6 >\cf4 \cb1 \
\cb3               \cf6 \{\cf8 /* Subject Input */\cf6 \}\cf4 \cb1 \
\cb3               \cf6 <\cf4 div className\cf6 =\cf7 "space-y-2"\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 label className\cf6 =\cf7 "text-xs text-gray-500 uppercase font-semibold tracking-wider"\cf6 >
\f1 \cf10 \'a5\'44\'c5\'e9\'b0\'ca\'a7\'40
\f0 \cf4  \cf6 /\cf4  \cf5 Subject\cf6 </\cf4 label\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 div className\cf6 =\cf7 "flex gap-2"\cf6 >\cf4 \cb1 \
\cb3                   \cf6 <\cf4 input\cb1 \
\cb3                     \cf2 type\cf6 =\cf7 "text"\cf4 \cb1 \
\cb3                     value\cf6 =\{\cf4 subject\cf6 \}\cf4 \cb1 \
\cb3                     onChange\cf6 =\{(\cf4 e\cf6 )\cf4  \cf6 =>\cf4  setSubject\cf6 (\cf4 e\cf6 .\cf4 target\cf6 .\cf4 value\cf6 )\}\cf4 \cb1 \
\cb3                     placeholder\cf6 =\cf7 "
\f1 \'a8\'d2\'a6\'70\'a1\'47\'bf\'df\'ab\'7d\'a6\'62\'ab\'ce\'b3\'bb\'a4\'57\'c5\'ce\'a4\'d3\'b6\'a7
\f0 "\cf4 \cb1 \
\cb3                     className\cf6 =\cf7 "flex-1 bg-gray-950 border border-gray-700 text-white text-base rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 block p-4 placeholder-gray-600 transition-all"\cf4 \cb1 \
\cb3                     onKeyDown\cf6 =\{(\cf4 e\cf6 )\cf4  \cf6 =>\cf4  e\cf6 .\cf4 key \cf6 ===\cf4  \cf7 'Enter'\cf4  \cf6 &&\cf4  handleGenerate\cf6 ()\}\cf4 \cb1 \
\cb3                   />\cb1 \
\cb3                   \cf6 <\cf4 button\cb1 \
\cb3                     onClick\cf6 =\{()\cf4  \cf6 =>\cf4  handleEnhance\cf6 (\cf7 'subject'\cf6 )\}\cf4 \cb1 \
\cb3                     disabled\cf6 =\{\cf4 isEnhancingSubject \cf6 ||\cf4  isGenerating \cf6 ||\cf4  \cf6 !\cf4 subject\cf6 \}\cf4 \cb1 \
\cb3                     className\cf6 =\cf7 "flex items-center justify-center gap-2 px-4 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"\cf4 \cb1 \
\cb3                     title\cf6 =\cf7 "Enhance subject description with AI"\cf4 \cb1 \
\cb3                   \cf6 >\cf4 \cb1 \
\cb3                     \cf6 \{\cf4 isEnhancingSubject \cf6 ?\cf4  \cf6 (\cf4 \cb1 \
\cb3                       \cf6 <\cf5 Sparkles\cf4  className\cf6 =\cf7 "w-5 h-5 animate-spin"\cf4  />\cb1 \
\cb3                     \cf6 )\cf4  \cf6 :\cf4  \cf6 (\cf4 \cb1 \
\cb3                       \cf6 <\cf5 Sparkles\cf4  className\cf6 =\cf7 "w-5 h-5"\cf4  />\cb1 \
\cb3                     \cf6 )\}\cf4 \cb1 \
\cb3                     \cf6 <\cf4 span className\cf6 =\cf7 "hidden sm:inline"\cf6 >\cf5 Enhance\cf6 </\cf4 span\cf6 >\cf4 \cb1 \
\cb3                   \cf6 </\cf4 button\cf6 >\cf4 \cb1 \
\cb3                 \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3               \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3               \cf6 \{\cf8 /* Location Input */\cf6 \}\cf4 \cb1 \
\cb3               \cf6 <\cf4 div className\cf6 =\cf7 "space-y-2"\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 label className\cf6 =\cf7 "text-xs text-gray-500 uppercase font-semibold tracking-wider"\cf6 >
\f1 \cf10 \'a6\'61\'c2\'49\'bb\'50\'a5\'fa\'bc\'76
\f0 \cf4  \cf6 /\cf4  \cf5 Environment\cf6 </\cf4 label\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 div className\cf6 =\cf7 "flex gap-2"\cf6 >\cf4 \cb1 \
\cb3                   \cf6 <\cf4 input\cb1 \
\cb3                     \cf2 type\cf6 =\cf7 "text"\cf4 \cb1 \
\cb3                     value\cf6 =\{\cf4 location\cf6 \}\cf4 \cb1 \
\cb3                     onChange\cf6 =\{(\cf4 e\cf6 )\cf4  \cf6 =>\cf4  setLocation\cf6 (\cf4 e\cf6 .\cf4 target\cf6 .\cf4 value\cf6 )\}\cf4 \cb1 \
\cb3                     placeholder\cf6 =\cf7 "
\f1 \'a8\'d2\'a6\'70\'a1\'47\'a6\'61\'a4\'a4\'ae\'fc\'a4\'70\'ae\'71
\f0 , 
\f1 \'a5\'bf\'a4\'c8\'b6\'a7\'a5\'fa
\f0 "\cf4 \cb1 \
\cb3                     className\cf6 =\cf7 "flex-1 bg-gray-950 border border-gray-700 text-white text-base rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 block p-4 placeholder-gray-600 transition-all"\cf4 \cb1 \
\cb3                     onKeyDown\cf6 =\{(\cf4 e\cf6 )\cf4  \cf6 =>\cf4  e\cf6 .\cf4 key \cf6 ===\cf4  \cf7 'Enter'\cf4  \cf6 &&\cf4  handleGenerate\cf6 ()\}\cf4 \cb1 \
\cb3                   />\cb1 \
\cb3                   \cf6 <\cf4 button\cb1 \
\cb3                     onClick\cf6 =\{()\cf4  \cf6 =>\cf4  handleEnhance\cf6 (\cf7 'environment'\cf6 )\}\cf4 \cb1 \
\cb3                     disabled\cf6 =\{\cf4 isEnhancingLocation \cf6 ||\cf4  isGenerating \cf6 ||\cf4  \cf6 !\cf4 location\cf6 \}\cf4 \cb1 \
\cb3                     className\cf6 =\cf7 "flex items-center justify-center gap-2 px-4 bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"\cf4 \cb1 \
\cb3                     title\cf6 =\cf7 "Enhance environment description with AI"\cf4 \cb1 \
\cb3                   \cf6 >\cf4 \cb1 \
\cb3                     \cf6 \{\cf4 isEnhancingLocation \cf6 ?\cf4  \cf6 (\cf4 \cb1 \
\cb3                       \cf6 <\cf5 Sparkles\cf4  className\cf6 =\cf7 "w-5 h-5 animate-spin"\cf4  />\cb1 \
\cb3                     \cf6 )\cf4  \cf6 :\cf4  \cf6 (\cf4 \cb1 \
\cb3                       \cf6 <\cf5 Sparkles\cf4  className\cf6 =\cf7 "w-5 h-5"\cf4  />\cb1 \
\cb3                     \cf6 )\}\cf4 \cb1 \
\cb3                     \cf6 <\cf4 span className\cf6 =\cf7 "hidden sm:inline"\cf6 >\cf5 Enhance\cf6 </\cf4 span\cf6 >\cf4 \cb1 \
\cb3                   \cf6 </\cf4 button\cf6 >\cf4 \cb1 \
\cb3                 \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3               \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3             \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3             \cf6 <\cf4 div className\cf6 =\cf7 "mt-6 flex justify-end"\cf6 >\cf4 \cb1 \
\cb3                \cf6 <\cf4 button\cb1 \
\cb3                 onClick\cf6 =\{\cf4 handleGenerate\cf6 \}\cf4 \cb1 \
\cb3                 disabled\cf6 =\{\cf4 isGenerating \cf6 ||\cf4  \cf6 !\cf4 subject\cf6 \}\cf4 \cb1 \
\cb3                 className\cf6 =\cf7 "w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-900/20 transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:hover:scale-100"\cf4 \cb1 \
\cb3               \cf6 >\cf4 \cb1 \
\cb3                 \cf6 \{\cf4 isGenerating \cf6 ?\cf4  \cf6 (\cf4 \cb1 \
\cb3                   \cf6 <\cf5 Sparkles\cf4  className\cf6 =\cf7 "w-5 h-5 animate-spin"\cf4  />\cb1 \
\cb3                 \cf6 )\cf4  \cf6 :\cf4  \cf6 (\cf4 \cb1 \
\cb3                   \cf6 <\cf5 Wand2\cf4  className\cf6 =\cf7 "w-5 h-5"\cf4  />\cb1 \
\cb3                 \cf6 )\}\cf4 \cb1 \
\cb3                 \cf6 \{\cf4 isGenerating \cf6 ?\cf4  \cf7 'Translating & Generating...'\cf4  \cf6 :\cf4  \cf7 '
\f1 \'a5\'cd\'a6\'a8\'c2\'bd\'c4\'b6\'b4\'a3\'a5\'dc\'b5\'fc
\f0 '\cf6 \}\cf4 \cb1 \
\cb3               \cf6 </\cf4 button\cf6 >\cf4 \cb1 \
\cb3             \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3           \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3           \cf6 \{\cf8 /* Results Section */\cf6 \}\cf4 \cb1 \
\cb3           \cf6 \{\cf4 results \cf6 &&\cf4  \cf6 (\cf4 \cb1 \
\cb3             \cf6 <\cf4 div className\cf6 =\cf7 "space-y-6 animate-fade-in"\cf6 >\cf4 \cb1 \
\cb3               \cf6 \{\cf8 /* Translation Check */\cf6 \}\cf4 \cb1 \
\cb3               \cf6 <\cf4 div className\cf6 =\cf7 "grid grid-cols-1 md:grid-cols-2 gap-4"\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 div className\cf6 =\cf7 "bg-gray-900/30 border border-gray-800 rounded-lg p-4"\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 h4 className\cf6 =\cf7 "text-sm font-semibold text-gray-300 mb-1"\cf6 >
\f2 \cf10 \uc0\u55357 \u56541 
\f0 \cf4  
\f1 \cf10 \'c2\'bd\'c4\'b6\'b9\'ef\'b7\'d3
\f0 \cf4  \cf6 (\cf5 Keywords\cf6 )</\cf4 h4\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 p className\cf6 =\cf7 "text-sm text-gray-500"\cf6 >\cf5 CN\cf6 :\cf4  \cf6 \{\cf4 results\cf6 .\cf4 translation\cf6 .\cf4 subject\cf6 .\cf4 original\cf6 \}</\cf4 p\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 p className\cf6 =\cf7 "text-sm text-indigo-400"\cf6 >\cf5 EN\cf6 :\cf4  \cf6 \{\cf4 results\cf6 .\cf4 translation\cf6 .\cf4 subject\cf6 .\cf4 translated\cf6 \}</\cf4 p\cf6 >\cf4 \cb1 \
\cb3                 \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf4 div className\cf6 =\cf7 "bg-gray-900/30 border border-gray-800 rounded-lg p-4"\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 h4 className\cf6 =\cf7 "text-sm font-semibold text-gray-300 mb-1"\cf6 >
\f2 \cf10 \uc0\u55356 \u57101 
\f0 \cf4  
\f1 \cf10 \'c2\'bd\'c4\'b6\'b9\'ef\'b7\'d3
\f0 \cf4  \cf6 (\cf5 Environment\cf6 )</\cf4 h4\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 p className\cf6 =\cf7 "text-sm text-gray-500"\cf6 >\cf5 CN\cf6 :\cf4  \cf6 \{\cf4 results\cf6 .\cf4 translation\cf6 .\cf4 location\cf6 .\cf4 original\cf6 \}</\cf4 p\cf6 >\cf4 \cb1 \
\cb3                    \cf6 <\cf4 p className\cf6 =\cf7 "text-sm text-indigo-400"\cf6 >\cf5 EN\cf6 :\cf4  \cf6 \{\cf4 results\cf6 .\cf4 translation\cf6 .\cf4 location\cf6 .\cf4 translated\cf6 \}</\cf4 p\cf6 >\cf4 \cb1 \
\cb3                 \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3               \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3               \cf6 <\cf4 div className\cf6 =\cf7 "grid gap-6"\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf5 ResultCard\cf4 \cb1 \
\cb3                   \cf2 type\cf6 =\cf7 "t2i"\cf4 \cb1 \
\cb3                   title\cf6 =\cf7 "Step 1: T2I (Kling/Midjourney) + Negative"\cf4 \cb1 \
\cb3                   content\cf6 =\{\cf4 results\cf6 .\cf4 t2i\cf6 \}\cf4 \cb1 \
\cb3                   description\cf6 =\cf7 "Use this prompt to generate your base image first. Negative prompt is included."\cf4 \cb1 \
\cb3                 />\cb1 \
\cb3                 \cb1 \
\cb3                 \cf6 <\cf5 ResultCard\cf4 \cb1 \
\cb3                   \cf2 type\cf6 =\cf7 "i2v"\cf4 \cb1 \
\cb3                   title\cf6 =\cf7 "Step 2: I2V (Runway/Kling) + Negative"\cf4 \cb1 \
\cb3                   content\cf6 =\{\cf4 results\cf6 .\cf4 i2v\cf6 \}\cf4 \cb1 \
\cb3                   description\cf6 =\cf7 "Upload the generated image and use this for motion control. Negative prompt is included."\cf4 \cb1 \
\cb3                 />\cb1 \
\cb3               \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\
\cb3               \cf6 <\cf4 div className\cf6 =\cf7 "flex items-start gap-3 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl"\cf6 >\cf4 \cb1 \
\cb3                 \cf6 <\cf5 Info\cf4  className\cf6 =\cf7 "w-5 h-5 text-blue-400 shrink-0 mt-0.5"\cf4  />\cb1 \
\cb3                 \cf6 <\cf4 p className\cf6 =\cf7 "text-sm text-blue-300"\cf6 >\cf4 \cb1 \
\cb3                   \cf6 <\cf4 strong\cf6 >\cf5 Pro\cf4  \cf5 Tip\cf4 :</strong\cf6 >\cf4  \cf5 For\cf4  the best results \cf2 in\cf4  \cf5 Runway\cf4  \cf5 Gen\cf6 -\cf9 3\cf4  or \cf5 Kling\cf7 's Image-to-Video mode, \cf4 \cb1 \
\cb3                   always upload the high\cf6 -\cf4 quality image generated \cf2 from\cf4  \cf5 Step\cf4  \cf9 1\cf4  \cf2 as\cf4  your reference\cf6 .\cf4  \cb1 \
\cb3                   \cf5 This\cf4  ensures character consistency and visual fidelity\cf6 .\cf4 \cb1 \
\cb3                 \cf6 </\cf4 p\cf6 >\cf4 \cb1 \
\cb3               \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3             \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3           \cf6 )\}\cf4 \cb1 \
\cb3         \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3       \cf6 </\cf4 main\cf6 >\cf4 \cb1 \
\cb3     \cf6 </\cf4 div\cf6 >\cf4 \cb1 \
\cb3   \cf6 );\cf4 \cb1 \
\cf6 \cb3 \};\cf4 \cb1 \
\
\cf2 \cb3 export\cf4  \cf2 default\cf4  \cf5 App\cf6 ;\cf4 \cb1 \
}