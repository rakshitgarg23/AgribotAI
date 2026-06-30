# chatbot.py - Enhanced AI-Powered Chatbot Engine for Water Management
import re
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ChatResponse:
    domain: str
    answer: str
    confidence: float
    suggestions: List[str]
    context: Dict = field(default_factory=dict)

class AdvancedWaterManagementBot:
    """Advanced AI-powered handler for water management queries with contextual awareness"""
    
    def __init__(self):
        self.conversation_context = {}
        self.user_preferences = {}
        
    # Enhanced Knowledge Base
    KNOWLEDGE_BASE = {
        "water_conservation": {
            "tips": [
                "Fix leaky faucets (can save 90 gallons/month)",
                "Install low-flow showerheads (saves ~25% water)",
                "Use drought-resistant plants for landscaping",
                "Collect rainwater for irrigation",
                "Run full loads in dishwashers and washing machines",
                "Turn off tap while brushing (saves 4 gallons/minute)",
                "Use a broom instead of hose to clean driveways",
                "Install water-efficient showerheads (2.5 GPM or less)"
            ],
            "outdoor": [
                "Water plants early morning or late evening to reduce evaporation",
                "Use mulch around plants to retain soil moisture",
                "Install drip irrigation systems (90% efficient vs 50% for sprinklers)",
                "Group plants with similar water needs together",
                "Use rain barrels to collect roof runoff"
            ],
            "appliances": [
                "Energy Star dishwashers use 4 gallons/cycle vs 10+ for hand washing",
                "High-efficiency washing machines use 15-30 gallons vs 40+ for older models",
                "Tankless water heaters save water by heating instantly",
                "Water-efficient toilets use 1.28 GPF vs 3.5+ for old models"
            ],
            "savings_calculator": {
                "leaky_faucet": "1 drip/sec = 3,000 gallons/year",
                "running_toilet": "200-400 gallons/day wasted",
                "long_shower": "Shorter by 2 mins = 500 gallons/year saved"
            }
        },
        
        "water_quality": {
            "ph_levels": {
                "optimal": "6.5 - 8.5",
                "low": "Below 6.5: Corrosive, may leach metals",
                "high": "Above 8.5: Hard water, bitter taste"
            },
            "contaminants": {
                "biological": ["E. coli", "Giardia", "Cryptosporidium", "Legionella"],
                "chemical": ["Lead", "Nitrate", "Arsenic", "PFAS", "Chlorine"],
                "physical": ["Sediment", "Turbidity", "Color", "Odor"]
            },
            "testing_methods": {
                "home_kit": "Test strips for basic parameters ($20-50)",
                "lab_testing": "Comprehensive analysis ($100-300)",
                "parameters": "pH, TDS, hardness, chlorine, bacteria, heavy metals"
            },
            "treatment_methods": {
                "activated_carbon": "Removes chlorine, VOCs, bad taste/smell",
                "reverse_osmosis": "Removes 95-99% of contaminants",
                "uv_purification": "Kills bacteria and viruses",
                "distillation": "Removes almost all impurities",
                "ion_exchange": "Softens hard water"
            }
        },
        
        "usage_monitoring": {
            "statistics": {
                "daily_avg_household": "300 gallons",
                "per_capita_usa": "82 gallons/day",
                "per_capita_world": "50 gallons/day",
                "indoor_vs_outdoor": "Indoor 60% | Outdoor 40%"
            },
            "fixture_breakdown": {
                "toilet": "24% (70-90 gallons/day)",
                "shower": "20% (60-80 gallons/day)",
                "faucet": "19% (50-70 gallons/day)",
                "washing_machine": "17% (40-60 gallons/day)",
                "leaks": "12% (30-50 gallons/day)",
                "other": "8% (25-35 gallons/day)"
            },
            "leak_detection": {
                "toilet_test": "Add food coloring to tank - if bowl shows color in 10 mins, you have a leak",
                "meter_test": "Turn off all water, check meter - if it moves, you have a leak",
                "audible_leaks": "Listen for running water when all fixtures are off"
            }
        },
        
        "rainwater_harvesting": {
            "benefits": [
                "Reduces water bills by 30-50%",
                "Provides chemical-free water for gardens",
                "Reduces stormwater runoff and erosion",
                "Emergency backup water supply"
            ],
            "calculation": "1 inch of rain on 1,000 sq ft roof = 600 gallons collected",
            "components": [
                "Catchment surface (roof)",
                "Gutters and downspouts",
                "Leaf screens and first-flush diverters",
                "Storage tank (rain barrel/cistern)",
                "Overflow mechanism",
                "Distribution system"
            ]
        },
        
        "fog_harvesting": {
            "how_it_works": "Fog collectors use mesh netting to capture water droplets from fog, which then drip into collection troughs",
            "efficiency": "Standard mesh collects 2-10 liters/m²/day, advanced meshes collect 15-25 liters/m²/day",
            "ideal_conditions": [
                "Coastal areas with frequent fog",
                "Mountainous regions with cloud forests",
                "Humidity > 70%",
                "Wind speed 10-20 km/h"
            ]
        },
        
        "regulations": {
            "epa": {
                "sdwa": "Safe Drinking Water Act (1974) - sets maximum contaminant levels",
                "cwa": "Clean Water Act - regulates pollutant discharges",
                "reporting": "Annual Consumer Confidence Reports required for water utilities"
            },
            "international": {
                "who": "WHO Guidelines for Drinking-water Quality",
                "eu": "EU Drinking Water Directive - stricter standards than US"
            }
        },
        
        "smart_water_tech": {
            "iot_devices": [
                "Smart water meters with real-time monitoring",
                "Leak detection sensors (alert you immediately)",
                "Smart irrigation controllers (weather-based watering)",
                "Water quality sensors (pH, TDS, turbidity)"
            ],
            "ai_applications": [
                "Predictive leak detection using pressure patterns",
                "Demand forecasting for water utilities",
                "Water quality prediction models",
                "Automated irrigation optimization"
            ]
        }
    }
    
    # Enhanced keyword mapping with synonyms and context
    KEYWORDS = {
        "water_conservation": {
            "primary": ["save water", "conserve", "drought", "efficient", "reduce usage", "waste water", "saving"],
            "specific": ["shower", "faucet", "leak", "drip", "toilet", "lawn", "garden"]
        },
        "water_quality": {
            "primary": ["quality", "test", "ph", "contaminated", "filter", "clean", "safe", "drink", "taste"],
            "specific": ["lead", "bacteria", "chlorine", "hard water", "softener", "purify"]
        },
        "usage_monitoring": {
            "primary": ["usage", "consumption", "bill", "meter", "how much", "gallons", "spent", "cost"],
            "specific": ["average", "bathroom", "kitchen", "laundry"]
        },
        "rainwater_harvesting": {
            "primary": ["rain", "rainwater", "harvest", "barrel", "cistern", "collection", "runoff"],
            "specific": ["gutter", "downspout", "storage", "tank"]
        },
        "fog_harvesting": {
            "primary": ["fog", "dew", "atmospheric", "humidity collection", "air water"],
            "specific": ["mesh", "net", "condensation"]
        },
        "smart_water_tech": {
            "primary": ["smart", "iot", "sensor", "automated", "monitoring system", "tech"],
            "specific": ["app", "tracker", "device", "controller"]
        },
        "regulations": {
            "primary": ["regulation", "law", "legal", "compliance", "standard", "permission", "epa"],
            "specific": ["rule", "requirement", "permit", "legal"]
        }
    }
    
    def handle(self, query: str, session_id: str = None) -> Optional[ChatResponse]:
        """Process water management queries with context awareness"""
        query_lower = query.lower()
        
        # Detect intent with weighted scoring
        detected_intent, score = self._detect_intent(query_lower)
        
        if not detected_intent:
            return self._handle_general_query(query_lower)
            
        # Generate contextual response
        response = self._generate_response(detected_intent, query_lower)
        
        # Add context about specific parameters if any
        context = self._extract_context(query_lower, detected_intent)
        
        return ChatResponse(
            domain=f"water_management_{detected_intent}",
            answer=response,
            confidence=min(score, 1.0),
            suggestions=self._get_smart_suggestions(detected_intent, query_lower),
            context=context
        )
    
    def _detect_intent(self, query: str) -> Tuple[Optional[str], float]:
        """Detect intent using weighted keyword matching"""
        intent_scores = {}
        
        for intent, keywords in self.KEYWORDS.items():
            score = 0
            # Primary keywords (weight: 2)
            for kw in keywords.get("primary", []):
                if kw in query:
                    score += 2
            # Specific keywords (weight: 1)
            for kw in keywords.get("specific", []):
                if kw in query:
                    score += 1
            
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return None, 0
        
        # Get intent with highest score
        best_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[best_intent]
        
        # Normalize score (max possible is ~5-6)
        normalized_score = min(max_score / 6, 1.0)
        
        return best_intent, normalized_score
    
    def _generate_response(self, intent: str, query: str) -> str:
        """Generate rich, contextual response with emojis and formatting"""
        
        responses = {
            "water_conservation": self._handle_conservation,
            "water_quality": self._handle_quality,
            "usage_monitoring": self._handle_monitoring,
            "rainwater_harvesting": self._handle_rainwater,
            "fog_harvesting": self._handle_fog,
            "smart_water_tech": self._handle_smart_tech,
            "regulations": self._handle_regulations
        }
        
        handler = responses.get(intent)
        if handler:
            return handler(query)
        
        return self._handle_general_response(query)
    
    def _handle_conservation(self, query: str) -> str:
        """Handle water conservation queries"""
        
        if "shower" in query:
            return "🚿 **Low-flow showerheads** can reduce shower water use by 25-60% (2.5 to 1.0 GPM).\n\n💰 For a family of 4, annual savings: **~$100 + 12,000 gallons**\n\n💡 Pro tip: A 5-minute shower uses 10-15 gallons vs 30+ for a bath!"
        
        if "leak" in query or "drip" in query:
            return "🔍 **Leak Detection Guide:**\n\n• **Dripping faucet** (1 drip/sec): 3,000 gallons/year\n• **Running toilet**: 200-400 gallons/day\n• **Hidden leaks**: Check your water meter before/after 2 hours of no usage\n\n🛠️ Most leaks are easy to fix with a $5 repair kit!"
        
        if "toilet" in query:
            return "🚽 **Toilet Water Efficiency:**\n\n• Old toilets: 3.5-7 gallons per flush (GPF)\n• Modern efficient: 1.28 GPF (save 70%)\n• Dual-flush: 0.8-1.6 GPF\n\n💰 Annual savings per toilet switching from 3.5 to 1.28 GPF: **12,000-15,000 gallons + $150-200**"
        
        if "outdoor" in query or "garden" in query or "lawn" in query:
            return "🌿 **Outdoor Water Conservation:**\n\n" + "\n".join(f"• {tip}" for tip in self.KNOWLEDGE_BASE["water_conservation"]["outdoor"][:4])
        
        # General conservation tips with variety
        tips = random.sample(self.KNOWLEDGE_BASE["water_conservation"]["tips"], min(4, len(self.KNOWLEDGE_BASE["water_conservation"]["tips"])))
        return "💧 **Top Water Conservation Tips:**\n\n" + "\n".join(f"• {tip}" for tip in tips) + "\n\n💡 Want specific advice about showers, toilets, leaks, or outdoor watering?"
    
    def _handle_quality(self, query: str) -> str:
        """Handle water quality queries"""
        
        if "ph" in query:
            ph_info = self.KNOWLEDGE_BASE["water_quality"]["ph_levels"]
            return f"🧪 **Water pH Explained:**\n\n• **Optimal range**: {ph_info['optimal']}\n• ⚠️ {ph_info['low']}\n• ⚠️ {ph_info['high']}\n\n💡 You can test pH with strips ($10-20) or digital meters ($30-100)"
        
        if "filter" in query or "purify" in query:
            treatment = self.KNOWLEDGE_BASE["water_quality"]["treatment_methods"]
            return "🔧 **Water Treatment Options:**\n\n" + "\n".join(f"• **{k.replace('_', ' ').title()}**: {v}" for k, v in treatment.items()) + "\n\n💡 Choose based on your specific contaminants - test first!"
        
        if "lead" in query:
            return "⚠️ **Lead in Water:**\n\n• No safe level for children/pregnancy\n• Common in older homes (pre-1986 pipes)\n• Testing: $20-50 for lead-specific kit\n• Solutions: NSF 53 certified filters or whole-house treatment\n\n🏠 Get your water tested if your home was built before 1986!"
        
        if "hard" in query:
            return "💎 **Hard Water Info:**\n\n• Caused by calcium and magnesium\n• Signs: soap scum, scale buildup, dry skin\n• Solutions: Water softener (ion exchange)\n• Benefits of soft water: longer appliance life, better soap lather\n\n💰 Water softeners cost $500-2000 installed"
        
        # General quality info
        return "🔬 **Water Quality Basics:**\n\n• **pH**: Should be 6.5-8.5\n• **Common contaminants**: Lead, Bacteria, Nitrates\n• **Testing**: Home kits ($20-50) or professional labs ($100-300)\n\n💡 Ask me about pH, filters, lead, or hard water for more details!"
    
    def _handle_monitoring(self, query: str) -> str:
        """Handle usage monitoring queries"""
        
        if "average" in query:
            stats = self.KNOWLEDGE_BASE["usage_monitoring"]["statistics"]
            return f"📊 **Water Usage Statistics:**\n\n• Average US household: {stats['daily_avg_household']}\n• Per capita (USA): {stats['per_capita_usa']}\n• Per capita (World): {stats['per_capita_world']}\n• Split: {stats['indoor_vs_outdoor']}\n\n💡 Track your usage to identify savings opportunities!"
        
        if "meter" in query:
            return "📏 **How to Read Your Water Meter:**\n\n1. Find your meter (usually near street or basement)\n2. Record the numbers (ignore red/zero-moving dials)\n3. Check again after 2 hours of no water use\n4. If numbers changed → you have a leak!\n\n💡 Most meters show cubic feet or gallons (1 cubic foot = 7.48 gallons)"
        
        if "cost" in query or "bill" in query:
            return "💰 **Water Cost Breakdown:**\n\n• Average US water bill: $70-100/month\n• Typical rate: $0.004-0.015 per gallon\n• Sewer charges often double the cost\n• Top savings: Fix leaks (10-15% of bill)\n\n💡 A family of 4 can save $200-500/year with conservation!"
        
        # General monitoring info
        breakdown = self.KNOWLEDGE_BASE["usage_monitoring"]["fixture_breakdown"]
        return "🏠 **Where Your Water Goes:**\n\n" + "\n".join(f"• **{k.replace('_', ' ').title()}**: {v}" for k, v in list(breakdown.items())[:4]) + "\n\n💡 Ask about finding leaks, reading meters, or reducing bills!"
    
    def _handle_rainwater(self, query: str) -> str:
        """Handle rainwater harvesting queries"""
        
        if "calculate" in query or "how much" in query:
            return "📐 **Rainwater Harvesting Calculation:**\n\n" + self.KNOWLEDGE_BASE["rainwater_harvesting"]["calculation"] + "\n\n**Example:** 1,000 sq ft roof × 1 inch rain × 0.6 = 600 gallons!\n\n💡 Most rain barrels hold 50-100 gallons - use multiple for more storage"
        
        if "benefit" in query or "advantage" in query:
            benefits = self.KNOWLEDGE_BASE["rainwater_harvesting"]["benefits"]
            return "✅ **Benefits of Rainwater Harvesting:**\n\n" + "\n".join(f"• {b}" for b in benefits)
        
        return "🌧️ **Rainwater Harvesting 101:**\n\n" + "\n".join(f"• {comp}" for comp in self.KNOWLEDGE_BASE["rainwater_harvesting"]["components"][:5]) + f"\n\n**Collection formula:** {self.KNOWLEDGE_BASE['rainwater_harvesting']['calculation']}\n\n💡 Ask about benefits, calculations, or specific components!"
    
    def _handle_fog(self, query: str) -> str:
        """Handle fog harvesting queries"""
        
        return "🌫️ **Fog Harvesting Explained:**\n\n" + f"• {self.KNOWLEDGE_BASE['fog_harvesting']['how_it_works']}\n\n**Efficiency:** {self.KNOWLEDGE_BASE['fog_harvesting']['efficiency']}\n\n**Ideal Conditions:**\n" + "\n".join(f"  • {cond}" for cond in self.KNOWLEDGE_BASE['fog_harvesting']['ideal_conditions']) + "\n\n💡 Best suited for coastal and high-altitude foggy regions (like parts of Chile, Peru, Morocco, and India's northeastern hills!)"
    
    def _handle_smart_tech(self, query: str) -> str:
        """Handle smart water technology queries"""
        
        iot_devices = self.KNOWLEDGE_BASE["smart_water_tech"]["iot_devices"]
        ai_apps = self.KNOWLEDGE_BASE["smart_water_tech"]["ai_applications"]
        
        return "🤖 **Smart Water Technology:**\n\n**IoT Devices Available:**\n" + "\n".join(f"  • {device}" for device in iot_devices[:3]) + "\n\n**AI Applications:**\n" + "\n".join(f"  • {app}" for app in ai_apps[:3]) + "\n\n💡 Smart systems typically pay for themselves in 1-2 years through water savings!"
    
    def _handle_regulations(self, query: str) -> str:
        """Handle regulations queries"""
        
        if "epa" in query or "safe drinking" in query:
            epa = self.KNOWLEDGE_BASE["regulations"]["epa"]
            return f"⚖️ **EPA Water Regulations:**\n\n• **Safe Drinking Water Act**: {epa['sdwa']}\n• **Clean Water Act**: {epa['cwa']}\n• **Reporting**: {epa['reporting']}\n\n💡 Water utilities must provide annual water quality reports on request"
        
        return "🌍 **Water Regulations Overview:**\n\n**US (EPA):** Safe Drinking Water Act, Clean Water Act\n**International:** WHO Guidelines, EU Directive\n\n**Key Requirements:**\n• Regular water quality testing\n• Consumer Confidence Reports\n• Contaminant level compliance\n\n💡 Ask specifically about EPA standards or international regulations!"
    
    # ── Basic / conversational command bank ───────────────────────────────────
    GREETINGS = [
        "👋 Hello there! I'm **AquaBot**, your AI Water Management Assistant.\n\nI can help you with:\n💧 Conservation tips\n🔬 Water quality\n📊 Usage monitoring\n🌧️ Rainwater harvesting\n🌫️ Fog collection\n🤖 Smart water tech\n⚖️ Regulations\n\nWhat would you like to know about water management?",
        "💧 Hi! Great to see you! I'm **AquaBot** — ask me anything about water conservation, quality, leaks, harvesting, or smart tech.",
        "🌊 Hey! I'm **AquaBot**, your water management expert. Ready to help you save water, test quality, or explore smart solutions!",
    ]

    HOW_ARE_YOU = [
        "😊 I'm doing great, thanks for asking! Always happy to talk about water management. What can I help you with today?",
        "💙 Flowing along perfectly, thanks! Ready to dive into any water topic you have in mind.",
        "🌊 Splashing along wonderfully! How about you? Got any water questions I can help with?",
    ]

    BOT_JOKES = [
        "💧 Why did the river break up with the lake?\n\nBecause it felt like the relationship was going *downstream*! 😄\n\n...Okay, back to saving water!",
        "🚿 What did the ocean say to the beach?\n\nNothing, it just *waved*! 🌊😄",
        "💦 Why is water so good at school?\n\nBecause it always goes with the *flow*! 😄",
        "🌧️ What do you call a wet bear?\n\nA *drizzly* bear! 🐻😄",
        "🚰 I tried to write a joke about water conservation… but I didn't want to *waste* your time! 😄",
    ]

    WATER_FACTS = [
        "🌍 **Wow Water Fact!**\n\nOnly **3%** of Earth's water is freshwater — and two-thirds of that is frozen in glaciers and ice caps. We all share the remaining 1%!",
        "🧠 **Did You Know?**\n\nA single leaky faucet (one drip per second) wastes over **3,000 gallons** of water per year — enough for 180 showers!",
        "🌊 **Amazing Fact!**\n\nWater is the **only natural substance** that exists in all three physical states — liquid, solid, and gas — at temperatures found naturally on Earth.",
        "🚰 **Water Fun Fact!**\n\nYou can survive roughly **3 weeks** without food, but only **3 days** without water. It makes up 60% of your body weight!",
        "💧 **Global Water Fact!**\n\nAgriculture uses about **70%** of the world's freshwater. One pound of beef requires approximately **1,800 gallons** to produce!",
        "🌧️ **Hydrological Fact!**\n\nThe water you drink today may have been **dinosaur pee** millions of years ago! Earth's water has been recycling through the water cycle for billions of years.",
    ]

    WATER_QUOTES = [
        "💬 *\"Water is the driving force of all nature.\"*\n— Leonardo da Vinci",
        "💬 *\"We never know the worth of water till the well is dry.\"*\n— Thomas Fuller",
        "💬 *\"In every walk with nature, one receives far more than he seeks.\"*\n— John Muir",
        "💬 *\"Water is life's matter and matrix, mother and medium.\"*\n— Albert Szent-Györgyi",
        "💬 *\"Pure water is the world's first and foremost medicine.\"*\n— Slovakian Proverb",
    ]

    FAREWELLS = [
        "👋 Goodbye! Remember — every drop counts. Stay hydrated and conserve water! 💧",
        "🌊 See you later! Keep saving water — the planet thanks you! 💙",
        "💧 Farewell! Don't forget: a 2-minute shorter shower saves ~500 gallons/year. Small actions, big impact! 🌍",
    ]

    HELP_MESSAGE = """🆘 **AquaBot Help Guide**

Here's everything I can help you with:

🌿 **Water Conservation**
  → "How can I save water at home?"
  → "Water saving tips for my garden"
  → "How much water does a leaky faucet waste?"

🔬 **Water Quality**
  → "How do I test my water quality?"
  → "What is the safe pH for drinking water?"
  → "How to remove lead from water?"

📊 **Usage Monitoring**
  → "How much water does the average household use?"
  → "How do I read my water meter?"
  → "Why is my water bill so high?"

🌧️ **Rainwater Harvesting**
  → "How does rainwater harvesting work?"
  → "How much water can I collect from my roof?"
  → "Benefits of a rain barrel?"

🌫️ **Fog Harvesting**
  → "What is fog harvesting?"
  → "Where does fog collection work best?"

🤖 **Smart Water Tech**
  → "What are smart water meters?"
  → "Can AI help detect leaks?"

⚖️ **Regulations**
  → "What are EPA water standards?"
  → "Is collecting rainwater legal?"

💬 **Just for Fun**
  → "Tell me a joke"
  → "Give me a water fact"
  → "Water quote"
  → "How are you?"

Just type your question naturally — I'll figure out what you need! 💙"""

    def _handle_general_query(self, query: str) -> ChatResponse:
        """Handle queries that don't match specific domain intent"""

        # ── How are you (check BEFORE generic greeting to avoid "hi" false match) ──
        how_are = ["how are you", "how r you", "how do you do", "how's it going",
                   "how are things", "you okay", "you good", "how you doing"]
        if any(w in query for w in how_are):
            return ChatResponse(
                domain="small_talk",
                answer=random.choice(self.HOW_ARE_YOU),
                confidence=1.0,
                suggestions=["Save water at home", "Water quality tips", "Tell me a joke"],
                context={}
            )

        # ── Bot identity (check BEFORE greeting) ──────────────────────────
        identity_words = ["who are you", "what are you", "your name", "about you",
                          "introduce yourself", "tell me about yourself", "are you a bot",
                          "are you ai", "are you human", "what is aquabot", "what's aquabot"]
        if any(w in query for w in identity_words):
            return ChatResponse(
                domain="identity",
                answer="🤖 I'm **AquaBot** — an AI-powered Water Management Assistant!\n\nI was built to help people:\n\n💧 **Conserve water** — tips for home, garden, and industry\n🔬 **Understand water quality** — pH, contaminants, filters\n📊 **Monitor usage** — meters, leaks, billing\n🌧️ **Harvest water** — rainwater and fog collection\n🤖 **Explore smart tech** — IoT sensors, AI-driven systems\n⚖️ **Navigate regulations** — EPA, WHO, and local laws\n\nThink of me as your personal water expert, available 24/7! 💙",
                confidence=1.0,
                suggestions=["What can you do?", "Give me water saving tips", "Tell me a fact"],
                context={}
            )

        # ── Random water facts (check BEFORE greeting) ─────────────────────
        fact_words = ["fact", "did you know", "tell me something", "interesting",
                      "fun fact", "random fact", "water fact", "trivia", "amaze me"]
        if any(w in query for w in fact_words):
            return ChatResponse(
                domain="education",
                answer=random.choice(self.WATER_FACTS),
                confidence=1.0,
                suggestions=["Another fact!", "Water conservation tips", "Tell me a joke"],
                context={}
            )

        # ── Thank you (check BEFORE greeting – "you" can match greeting words) ──
        thanks_words = ["thank", "thanks", "ty", "thx", "appreciate", "cheers",
                        "grateful", "much appreciated"]
        if any(w in query for w in thanks_words):
            return ChatResponse(
                domain="gratitude",
                answer=random.choice([
                    "💙 You're welcome! Remember — every drop counts. Ask me anything else!",
                    "😊 Happy to help! Water conservation is a team effort — you're doing great!",
                    "🌊 Anytime! Feel free to come back whenever you have more water questions.",
                ]),
                confidence=1.0,
                suggestions=["Water conservation tips", "Reduce water bill", "Fix leaks"],
                context={}
            )

        # ── Greetings ──────────────────────────────────────────────────────
        greet_words = ["hello", "hi", "hey", "howdy", "hiya", "sup", "what's up",
                       "good morning", "good afternoon", "good evening", "good day",
                       "greetings", "yo", "wassup", "namaste", "salut", "bonjour"]
        if any(w in query for w in greet_words):
            return ChatResponse(
                domain="greeting",
                answer=random.choice(self.GREETINGS),
                confidence=1.0,
                suggestions=["How to save water?", "Test water quality?", "Tell me a water fact"],
                context={}
            )

        # ── Farewells ──────────────────────────────────────────────────────
        bye_words = ["bye", "goodbye", "see you", "see ya", "later", "cya",
                     "farewell", "take care", "good night", "gotta go", "ttyl", "quit"]
        if any(w in query for w in bye_words):
            return ChatResponse(
                domain="farewell",
                answer=random.choice(self.FAREWELLS),
                confidence=1.0,
                suggestions=["Water saving tips", "Water quality", "Smart water tech"],
                context={}
            )

        # ── Help ───────────────────────────────────────────────────────────
        help_words = ["help", "what can you do", "commands", "menu", "options",
                      "what do you know", "capabilities", "features", "guide"]
        if any(w in query for w in help_words):
            return ChatResponse(
                domain="help",
                answer=self.HELP_MESSAGE,
                confidence=1.0,
                suggestions=["How to save water?", "Test water quality?", "Smart water tech?"],
                context={}
            )

        # ── Jokes ──────────────────────────────────────────────────────────
        joke_words = ["joke", "funny", "laugh", "humor", "humour", "pun", "make me smile",
                      "something funny", "entertain me"]
        if any(w in query for w in joke_words):
            return ChatResponse(
                domain="entertainment",
                answer=random.choice(self.BOT_JOKES),
                confidence=1.0,
                suggestions=["Another joke!", "Give me a water fact", "Conservation tips"],
                context={}
            )

        # ── Quotes ─────────────────────────────────────────────────────────
        quote_words = ["quote", "inspire", "motivation", "wisdom", "saying", "proverb"]
        if any(w in query for w in quote_words):
            return ChatResponse(
                domain="inspiration",
                answer=random.choice(self.WATER_QUOTES),
                confidence=1.0,
                suggestions=["Give me a water fact", "Water conservation tips", "Tell me a joke"],
                context={}
            )

        # ── Compliments to bot ─────────────────────────────────────────────
        compliment_words = ["good bot", "great bot", "nice bot", "amazing", "awesome",
                            "you're great", "you are great", "well done", "good job",
                            "you're helpful", "love you", "love this"]
        if any(w in query for w in compliment_words):
            return ChatResponse(
                domain="small_talk",
                answer=random.choice([
                    "🥰 Thank you so much! That really means a lot! Now, let's save some water together! 💧",
                    "😊 Aw, you're too kind! I'm just doing my part to help the planet, one drop at a time. 🌍",
                    "💙 Thanks! I love helping with water topics — it's kind of my thing! What would you like to explore?",
                ]),
                confidence=1.0,
                suggestions=["Water conservation tips", "Water quality", "Tell me a water fact"],
                context={}
            )

        # ── Yes / No / Okay ────────────────────────────────────────────────
        agree_words = ["yes", "yeah", "yep", "sure", "okay", "ok", "alright",
                       "sounds good", "got it", "understood", "cool", "great",
                       "perfect", "no", "nope", "nah", "not really", "no thanks"]
        if query.strip() in agree_words or query.strip() + "." in agree_words:
            return ChatResponse(
                domain="small_talk",
                answer="💧 Got it! Feel free to ask me anything about water management. I'm here to help!\n\nTry asking:\n• \"How can I save water at home?\"\n• \"What is rainwater harvesting?\"\n• \"Tell me a water fact\"",
                confidence=0.9,
                suggestions=["Water saving tips", "Water quality testing", "Tell me a joke"],
                context={}
            )

        # ── Weather tie-in ─────────────────────────────────────────────────
        weather_words = ["weather", "rain today", "drought", "flood", "monsoon",
                         "dry season", "climate change", "global warming"]
        if any(w in query for w in weather_words):
            return ChatResponse(
                domain="weather_water",
                answer="🌦️ **Weather & Water Management:**\n\nWeather patterns directly impact water availability!\n\n• **During droughts**: Conserve aggressively — fix leaks, water plants early morning, reduce lawn watering\n• **During heavy rain**: Rainwater harvesting is at its peak — great time to fill barrels and cisterns!\n• **Climate change** is making droughts longer and storms more intense, making water conservation more critical than ever\n• **Flood events** can contaminate water supplies — always test water quality after major flooding\n\n💡 Want tips tailored to your current weather situation?",
                confidence=0.9,
                suggestions=["Rainwater harvesting tips", "Drought water saving", "Water quality after flood"],
                context={}
            )

        # ── Crisis / emergency water ───────────────────────────────────────
        emergency_words = ["emergency", "no water", "water cut", "water outage",
                           "contaminated supply", "boil water", "water crisis", "disaster"]
        if any(w in query for w in emergency_words):
            return ChatResponse(
                domain="emergency",
                answer="🚨 **Emergency Water Guide:**\n\n**If you have no tap water:**\n• Use stored bottled water (1 gallon/person/day minimum)\n• Collect rainwater as a backup\n• Check with local authorities for emergency supply points\n\n**If water is contaminated:**\n• **Boil water** for at least 1 minute (3 min at altitude) before drinking\n• Use certified water filters (NSF 53 or NSF 58)\n• Don't use tap water for baby formula without boiling first\n\n**Emergency storage tips:**\n• Store at least **72 hours** (3 gallons/person) of water\n• Use food-grade containers in a cool, dark place\n• Rotate stored water every 6-12 months\n\n📞 Contact your local water utility or emergency services for specific guidance!",
                confidence=1.0,
                suggestions=["Water purification methods", "Rainwater harvesting", "Water quality testing"],
                context={}
            )

        # ── Compliment the user ────────────────────────────────────────────
        user_compliment_words = ["i want to save water", "i care about water",
                                 "trying to help", "want to conserve", "i recycle",
                                 "eco friendly", "i'm green", "environment"]
        if any(w in query for w in user_compliment_words):
            return ChatResponse(
                domain="encouragement",
                answer="🌟 That's fantastic! People like you make a real difference.\n\n🌍 If every household saved just **10 gallons/day**, the US alone would save **1 trillion gallons/year**.\n\nHere are your next steps to become a water conservation champion:\n\n1. 🔍 **Find & fix leaks** — biggest single impact\n2. 🚿 **Install low-flow fixtures** — save 25-60%\n3. 🌧️ **Harvest rainwater** — free garden water\n4. 📊 **Monitor your usage** — what gets measured gets managed\n5. 🤖 **Consider smart tech** — automate your savings\n\nWant details on any of these? 💙",
                confidence=1.0,
                suggestions=["How to find leaks?", "Install low-flow showerhead", "Start rainwater harvesting"],
                context={}
            )

        # ── Bored / just chatting ──────────────────────────────────────────
        bored_words = ["bored", "entertain me", "talk to me", "chat", "just talking",
                       "nothing to do", "what's new", "anything interesting"]
        if any(w in query for w in bored_words):
            return ChatResponse(
                domain="small_talk",
                answer=random.choice([
                    f"😄 Let me entertain you with this!\n\n{random.choice(self.WATER_FACTS)}\n\nOr ask me a question — I promise water topics are more exciting than they sound! 💧",
                    f"🎉 Ooh, let's have some fun!\n\n{random.choice(self.BOT_JOKES)}\n\nOr challenge me — ask anything about water!",
                    f"🌊 Fun fact incoming!\n\n{random.choice(self.WATER_FACTS)}\n\n...Pretty wild right? Ask me for more! 😊",
                ]),
                confidence=1.0,
                suggestions=["Tell me another fact!", "Tell me a joke", "Water saving challenge"],
                context={}
            )

        # ── Water saving challenge ─────────────────────────────────────────
        challenge_words = ["challenge", "goal", "target", "how do i start",
                           "where to begin", "water challenge", "30 day"]
        if any(w in query for w in challenge_words):
            return ChatResponse(
                domain="challenge",
                answer="🏆 **7-Day Water Saving Challenge!**\n\n**Day 1** 🔍 — Find & fix one leak\n**Day 2** 🚿 — Take a 5-minute shower (or shorter!)\n**Day 3** 🌱 — Water plants early morning only\n**Day 4** 🍽️ — Only run full dishwasher/washer loads\n**Day 5** 🪣 — Set up a rain barrel or bucket collection\n**Day 6** 🧹 — Use a broom instead of a hose outdoors\n**Day 7** 📊 — Read your water meter and calculate savings!\n\n💪 Estimated savings: **200-400 gallons** in one week!\n\nShare this challenge with friends and family for maximum impact! 🌍",
                confidence=1.0,
                suggestions=["How to fix a leak?", "Set up a rain barrel", "Track water usage"],
                context={}
            )

        # ── Default fallback ───────────────────────────────────────────────
        return ChatResponse(
            domain="general",
            answer="💧 I'm your water management expert! I can help with:\n\n• **Conservation** — Save water at home, garden & more\n• **Quality** — Testing, treatment, pH & contaminants\n• **Monitoring** — Track usage and find leaks\n• **Harvesting** — Rainwater and fog collection systems\n• **Smart Tech** — IoT sensors and AI-driven solutions\n• **Regulations** — EPA, WHO & international standards\n\nOr try: \"Tell me a joke\", \"Water fact\", \"Help\"\n\nWhat specific water topic interests you?",
            confidence=0.5,
            suggestions=["Save water at home", "Is my water safe?", "Tell me a water fact"],
            context={}
        )
    
    def _handle_general_response(self, query: str) -> str:
        """Fallback response generator"""
        return "💧 I can help you with water management topics! Try asking about:\n\n• Water conservation tips for home\n• Water quality testing methods\n• How to monitor usage and find leaks\n• Rainwater or fog harvesting systems\n• Smart water technology\n\nWhat would you like to learn about?"
    
    def _extract_context(self, query: str, intent: str) -> Dict:
        """Extract contextual information from query"""
        context = {}
        
        # Extract numerical values (gallons, percentages, etc.)
        numbers = re.findall(r'\d+(?:\.\d+)?', query)
        if numbers:
            context["mentioned_numbers"] = numbers
        
        # Extract location hints
        regions = ["home", "garden", "farm", "industry", "office", "school"]
        for region in regions:
            if region in query:
                context["setting"] = region
                break
        
        # Extract weather/climate hints
        climate_words = ["dry", "arid", "humid", "coastal", "mountain", "desert", "tropical"]
        for climate in climate_words:
            if climate in query:
                context["climate"] = climate
                break
        
        return context
    
    def _get_smart_suggestions(self, intent: str, query: str) -> List[str]:
        """Generate intelligent follow-up suggestions based on context"""
        
        suggestion_map = {
            "water_conservation": [
                "How can I detect hidden leaks?",
                "Best showerhead for water savings?",
                "Water-efficient appliances?",
                "Outdoor watering tips?"
            ],
            "water_quality": [
                "How to test water at home?",
                "What does a water filter remove?",
                "Is bottled water safer than tap?",
                "How to soften hard water?"
            ],
            "usage_monitoring": [
                "How to find my water meter?",
                "Average usage for family of 4?",
                "Smart water monitors explained",
                "How to lower water bill?"
            ],
            "rainwater_harvesting": [
                "What size rain barrel do I need?",
                "Is rainwater safe for vegetables?",
                "DIY rainwater system cost?",
                "Legal issues with collection?"
            ],
            "fog_harvesting": [
                "Where does fog harvesting work best?",
                "DIY fog collector design?",
                "Fog vs rainwater quality?",
                "Cost of fog harvesting systems?"
            ],
            "smart_water_tech": [
                "Best smart water monitor 2024?",
                "Can AI predict water leaks?",
                "Smart irrigation controllers?",
                "IoT water quality sensors?"
            ]
        }
        
        # Return context-specific suggestions
        base_suggestions = suggestion_map.get(intent, suggestion_map["water_conservation"])
        
        # Customize based on query keywords
        if "shower" in query:
            return ["Low-flow showerhead brands?", "Navy shower technique?", "Shower timer benefits?"]
        if "leak" in query:
            return ["How to fix toilet leak?", "Signs of slab leak?", "Leak detection companies?"]
        if "filter" in query:
            return ["RO vs carbon filter?", "Under sink vs whole house?", "Filter replacement schedule?"]
            
        return random.sample(base_suggestions, min(4, len(base_suggestions)))


class MultiDomainRouter:
    """Routes queries with context awareness"""
    
    def __init__(self):
        self.water_bot = AdvancedWaterManagementBot()
        self.session_contexts = {}
    
    def route(self, user_message: str, session_id: str = None) -> ChatResponse:
        """Route to appropriate handler with session context"""
        
        if not session_id:
            session_id = "default"
        
        # Handle with water management bot
        response = self.water_bot.handle(user_message, session_id)
        
        if response and response.confidence > 0.2:
            # Store context for follow-up
            if session_id not in self.session_contexts:
                self.session_contexts[session_id] = []
            self.session_contexts[session_id].append({
                "query": user_message,
                "response": response.answer,
                "domain": response.domain
            })
            return response
        
        # Fallback
        return ChatResponse(
            domain="general",
            answer="💧 I specialize in water management topics! Ask me about water conservation, quality testing, usage monitoring, rainwater harvesting, or fog collection. What would you like to know?",
            confidence=0.0,
            suggestions=["Water saving tips", "Water quality testing", "Smart water tech"],
            context={}
        )


class ChatBot:
    """Main chatbot interface with enhanced features"""
    
    def __init__(self):
        self.router = MultiDomainRouter()
        self.conversation_history = []
        self.stats = {
            "total_queries": 0,
            "domains_handled": {}
        }
    
    def chat(self, message: str, session_id: str = None) -> dict:
        """Main chat interface with analytics"""
        
        # Store history
        self.conversation_history.append({"role": "user", "content": message, "timestamp": datetime.now().isoformat()})
        
        # Get response
        response = self.router.route(message, session_id)
        
        # Update stats
        self.stats["total_queries"] += 1
        domain_key = response.domain.split("_")[1] if "_" in response.domain else response.domain
        self.stats["domains_handled"][domain_key] = self.stats["domains_handled"].get(domain_key, 0) + 1
        
        result = {
            "response": response.answer,
            "domain": response.domain,
            "confidence": round(response.confidence, 2),
            "suggestions": response.suggestions,
            "timestamp": datetime.now().isoformat(),
            "context": response.context
        }
        
        self.conversation_history.append({"role": "assistant", "content": response.answer, "timestamp": datetime.now().isoformat()})
        
        return result
    
    def get_water_stats(self) -> dict:
        """Quick reference data"""
        return {
            "daily_avg_household": "300 gallons",
            "cost_saving_potential": "$200-500/year with conservation",
            "crisis_threshold": "Below 1,000 gallons/person/year = water stress",
            "top_saver": "Fixing leaks (10% average household savings)",
            "global_scarcity": "2.2 billion people lack access to safe water",
            "agricultural_use": "70% of global freshwater used for agriculture"
        }
    
    def get_session_summary(self, session_id: str = None) -> dict:
        """Get summary of conversation session"""
        if session_id and session_id in self.router.session_contexts:
            history = self.router.session_contexts[session_id]
            return {
                "session_id": session_id,
                "total_exchanges": len(history),
                "last_query": history[-1]["query"] if history else None,
                "domains_discussed": list(set(h["domain"] for h in history))
            }
        return {"error": "Session not found"}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.router.session_contexts = {}
        return {"status": "History cleared"}