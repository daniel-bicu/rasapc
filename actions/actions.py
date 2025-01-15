from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted


class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I'm sorry, I didn't understand that. Could you please rephrase or provide more details?")
        # Optionally revert the last user input so the bot doesn’t get stuck.
        return [UserUtteranceReverted()]

class ActionSuggestPlacesByActivity(Action):
    def name(self) -> Text:
        return "action_suggestions_by_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        activity = tracker.get_slot("activity")
        print(f"Trying to suggest places for {activity}...")
          # Define suggestions for each activity
        suggestions = {
            "museums": ["Paris", "Rome", "New York", "London", "Tokyo"],
            "surfing": ["Hawaii", "Bali", "Gold Coast", "Cape Town", "Santa Cruz"],
            "ski": ["Aspen", "Whistler", "Zermatt", "Chamonix", "Banff"],
            "family trip": ["Orlando", "San Diego", "Tokyo Disney", "London", "Singapore"],
            "retreat": ["Bali", "Sedona", "Ibiza", "Goa", "Costa Rica"],
        }

        # Check if the activity is recognized
        if activity in suggestions:
            places = suggestions[activity]
            
            buttons = [
                {"title": place, "payload": f"/choose_place{{\"place\": \"{place}\"}}"} 
                for place in places
            ]
            
            # Send buttons to the user
            print("Options:")
            for button in buttons:
                print(button)
                
            dispatcher.utter_message(text=f"For {activity}, here are some great options:", buttons=buttons)
        else:
            dispatcher.utter_message(text="I couldn't find suggestions for that activity. Could you clarify or try another activity?")

        return []

class ActionSuggestAreas(Action):
    def name(self) -> Text:
        return "action_suggest_area_by_place_and_budget"

    def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Retrieve the user's choices
        place = tracker.get_slot("place")
        budget = tracker.get_slot("budget")


        print(f"Trying to suggest places for place: {place} and budget: {budget}...")
        # Define tours based on place and budget
        tours = {
            # museums
           "Paris": {
                "low": ["Walking tour of Montmartre", "Visit to free art exhibits"],
                "medium": ["Guided Louvre Museum tour", "Versailles Palace day trip"],
                "high": ["Private tour of Musée d'Orsay", "Exclusive wine and art experience"]
            },
            "Rome": {
                "low": ["Self-guided Colosseum tour", "Stroll through Trastevere"],
                "medium": ["Skip-the-line Vatican Museums tour", "Underground catacombs experience"],
                "high": ["Private Sistine Chapel tour", "Luxury Roman history and wine tour"]
            },
            "New York": {
                "low": ["Walking tour of Central Park", "Visit to free galleries in Chelsea"],
                "medium": ["Skip-the-line MoMA tickets", "Guided Metropolitan Museum of Art tour"],
                "high": ["Private VIP museum experience", "Exclusive Broadway and art package"]
            },
            "London": {
                "low": ["Visit to British Museum", "Walking tour of Southbank"],
                "medium": ["Guided National Gallery tour", "Tower of London and Crown Jewels package"],
                "high": ["Private art gallery tours", "Luxury London museum crawl"]
            },
            "Tokyo": {
                "low": ["Visit to free exhibits at Ueno Park", "Self-guided Asakusa cultural tour"],
                "medium": ["Guided Edo-Tokyo Museum tour", "Ghibli Museum experience"],
                "high": ["Private Samurai and art history tour", "Luxury Tokyo art and cuisine package"]
            },
            # surfing
            "Hawaii": {
                "low": ["Beach rental surfboards", "Community surf class"],
                "medium": ["Group surfing lessons", "Half-day surf safari"],
                "high": ["Private surf lessons with a pro", "Luxury beachfront surf retreat"]
            },
            "Bali": {
                "low": ["Beginner surfing class at Kuta Beach", "Beach day at Padang Padang"],
                "medium": ["Group surf lessons in Canggu", "Sunset surf safari"],
                "high": ["Private surf coaching session", "Exclusive surf resort stay"]
            },
            "Gold Coast": {
                "low": ["Beach board rental", "Learn-to-surf group class"],
                "medium": ["Guided surfing experience", "Half-day wave-riding session"],
                "high": ["Private surfing retreat", "Luxury oceanfront surfing package"]
            },
            "Cape Town": {
                "low": ["Surfboard rental at Muizenberg", "Budget group surf lessons"],
                "medium": ["Professional surfing workshop", "Cape Town surf day trip"],
                "high": ["Private pro coaching session", "Luxury surf and wine retreat"]
            },
            "Santa Cruz": {
                "low": ["Surfboard rental at Pleasure Point", "Community surf class"],
                "medium": ["Surf and yoga day camp", "Guided surfing experience"],
                "high": ["Private surfing retreat package", "Luxury surf lodge stay"]
            },
            # ski
            "Aspen": {
                "low": ["Snowshoe hiking tour", "Self-guided city tour"],
                "medium": ["Guided ski lessons", "Hot springs visit"],
                "high": ["Helicopter ski adventure", "Luxury spa package"]
            },
            "Whistler": {
                "low": ["Budget snowboarding session", "Self-guided snowshoe trail"],
                "medium": ["Group ski lessons", "Scenic gondola ride"],
                "high": ["Heli-skiing package", "Luxury mountain lodge stay"]
            },
            "Zermatt": {
                "low": ["Ski lift ticket for beginners", "Winter hiking trails"],
                "medium": ["Guided ski lessons", "Scenic Glacier Express experience"],
                "high": ["Private ski guide experience", "Luxury chalet stay"]
            },
            "Chamonix": {
                "low": ["Snowshoe tour of Mont Blanc", "Budget cable car ride"],
                "medium": ["Half-day skiing lessons", "Guided alpine adventure"],
                "high": ["Private glacier skiing", "Luxury Mont Blanc chalet experience"]
            },
            "Banff": {
                "low": ["Budget ski rental", "Snowshoe walk in Banff National Park"],
                "medium": ["Group ski lessons", "Hot springs experience"],
                "high": ["Helicopter glacier tour", "Luxury mountain resort stay"]
            },
            # family trip
            "Orlando": {
                "low": ["Day at a public park", "Budget theme park tickets"],
                "medium": ["Disney World day pass", "SeaWorld family package"],
                "high": ["VIP Disney experience", "Luxury villa with park passes"]
            },
            "San Diego": {
                "low": ["Visit to Balboa Park", "Self-guided zoo tour"],
                "medium": ["San Diego Zoo tickets", "SeaWorld family day"],
                "high": ["Private zoo tour", "Luxury beachside resort stay"]
            },
            "Tokyo Disney": {
                "low": ["Budget tickets for DisneySea", "Self-guided theme park tour"],
                "medium": ["Full-day Tokyo Disneyland experience", "Character dining experience"],
                "high": ["VIP Disney resort stay", "Private park guide package"]
            },
            "London": {
                "low": ["Visit to Hyde Park", "Walking tour of Tower Bridge"],
                "medium": ["London Eye family pass", "Madame Tussauds experience"],
                "high": ["Private Harry Potter studio tour", "Luxury family hotel stay"]
            },
            "Singapore": {
                "low": ["Gardens by the Bay self-guided visit", "Public park day"],
                "medium": ["Sentosa Island family package", "Singapore Zoo family experience"],
                "high": ["Luxury Universal Studios VIP experience", "Resort World Sentosa stay"]
            },
            # retreat
            "Bali": {
                "low": ["Local yoga class", "Beach meditation"],
                "medium": ["Group yoga retreat", "Wellness spa day"],
                "high": ["Luxury wellness retreat", "Exclusive villa with private spa"]
            },
            "Sedona": {
                "low": ["Self-guided red rock hike", "Local meditation session"],
                "medium": ["Guided vortex tour", "Wellness day retreat"],
                "high": ["Private healing retreat", "Luxury spa and wellness experience"]
            },
            "Ibiza": {
                "low": ["Beachside yoga", "Sunset meditation class"],
                "medium": ["Guided wellness retreat", "Mid-range spa package"],
                "high": ["Luxury private retreat", "Exclusive holistic healing package"]
            },
            "Goa": {
                "low": ["Local yoga class", "Beach meditation at Palolem"],
                "medium": ["Mid-range yoga and wellness retreat", "Spa and relaxation package"],
                "high": ["Luxury beachside retreat", "Private yoga villa experience"]
            },
            "Costa Rica": {
                "low": ["Self-guided rainforest hike", "Community yoga session"],
                "medium": ["Eco-lodge wellness retreat", "Group spa day"],
                "high": ["Luxury rainforest villa retreat", "Private wellness package"]
            }
        }

        # Generate recommendations
        if place in tours and budget in tours[place]:
            recommendations = tours[place][budget]
            message = f"Based on your budget ({budget}) in {place}, here are some great options: {', '.join(recommendations)}."
        else:
            message = f"Sorry, I couldn't find any tours for {place} with a {budget} budget. Try another option!"

        # Send the message to the user
        dispatcher.utter_message(text=message)

        return []    
    

class ActionSafetyTips(Action):
    def name(self) -> Text:
        return "action_safety_tips"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        place = tracker.get_slot("place")

        print(f"Trying to give safetyp tips for place: {place}")

        tips = {
            "Romania": ["Always keep your valuables secure.", "Be aware of pickpockets!"],
            "Paris": ["Keep away from rats.", "Be aware of pickpockets!", "Do not eat too much!"],
            "Rome": ["Carry a copy of your ID."]
        }
        tips = tips.get(place, ["Be aware of keeping your documents safe!"])
        dispatcher.utter_message(text=f"Here are some safety tips: {', '.join(tips)}")

        print("Tips offered: ", tips)

        return []
