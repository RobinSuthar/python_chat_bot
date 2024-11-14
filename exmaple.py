import openai
import dotenv
import os
import pygame
import speech_recognition as sr
from gtts import gTTS
import moviepy.editor as mp 
import threading
import tempfile
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

dotenv.load_dotenv()

class Question(BaseModel):
    question: str

openai.api_key = os.getenv("OPENAI_API_KEY")

store_data = {
    "store_name": "Highlander Wine & Spirits",
    "specialties": ["Wine", "Spirits", "Beer"],
    "exclusives": ["Highlander Wine & Spirits Exclusives", "Cellar Picks"],
    "offers": "Get a bonus offer of 10% off when you join our fantastic newsletter!",
    "loyalty_points": {
        "in_store": {
            "description": "Every dollar spent in-store earns 3 points. 100 points = $1.00, 1000 points = $10.00. Points never expire and can be redeemed at any time.",
            "eligibility": "Note: Corporate, preferential, or licensee discounts are not eligible for loyalty points."
        },
        "online": {
            "description": "Points can no longer be accumulated with online purchases as of September 30, 2021. Points from before this date can still be used for in-store purchases but are not redeemable online.",
            "disclaimer": "Points hold no cash value, are non-transferrable, and are provided 'as-is' without warranty."
        }
    },
    "vintage_disclaimer": (
        "Due to the Alberta Government distribution system, Highlander is unable to guarantee vintages. "
        "If a requested vintage cannot be fulfilled, you will be notified and can choose to accept the available vintage or cancel your order."
    ),
    "shipping_info": {
        "free_delivery": "Free delivery on orders over $150 within Calgary city limits.",
        "free_pickup": "Free in-store pickup at 8 stores throughout Calgary & Alberta.",
        "online_ordering": "We offer quick and efficient online ordering for wine, beer, and spirits."
    },
    "faq": {
        "sales_start_end": "Our weekly sales start on Monday and end the following Wednesday at 10 AM MST."
    },
    "contact_info": {
        "phone": "(403) 640-6220",
        "email": "contact us online",
        "sales_email_change": "To change the email address where you receive sales emails, open the last sales email you received and click 'Update Profile' at the bottom. Follow the instructions emailed to you to complete the update."
    },
    "employees": ["Brad", "Jose", "Jeswin", "Robin"],
    "creator": "Robin",
    "store_hours": {
        "mon_thurs": "9 AM - 9 PM",
        "fri_sat": "10 AM - 11 PM",
        "sun": "11 AM - 8 PM"
    },
    "employees": ["Brad", "Jose", "Jeswin", "Robin"],
    "creator": "Robin",
    "store_hours": {
        "mon_thurs": "9 AM - 9 PM",
        "fri_sat": "10 AM - 11 PM",
        "sun": "11 AM - 8 PM"
    },
    "website": "https://www.highlanderwine.com",
    "social_media": {
        "instagram": "https://www.instagram.com/highlanderwine",
        "facebook": "https://www.facebook.com/highlanderwine",
        "twitter": "https://twitter.com/highlanderwine"
    },
    "locations": [
        {
            "name": "Main Calgary Store",
            "address": "123 Main St, Calgary, AB T2P 1K3",
            "hours": "9 AM - 9 PM Mon-Thurs, 10 AM - 11 PM Fri-Sat, 11 AM - 8 PM Sun"
        },
        {
            "name": "Downtown Branch",
            "address": "456 Downtown Rd, Calgary, AB T2P 3H4",
            "hours": "10 AM - 8 PM Mon-Sun"
        }
    ],
    "online_services": [
        "Gift cards available for purchase online",
        "Virtual tastings and events",
        "Monthly newsletter with exclusive discounts and store news"
    ]
    
}

def highlander_assistant():
    print("Welcome to HighlanderBot! Ask me for wine, beer, or liquor recommendations. Type 'exit' to end the chat.")
    print(f"At {store_data['store_name']} in Calgary, we specialize in Wine, Spirits, and Beer.")
    print(f"Special offers: {store_data['offers']}")
    print(f"Need help? Contact us at {store_data['contact_info']['phone']} or email: {store_data['contact_info']['email']}")
    
    while True:
        user_input = input("You: ")
        

        if user_input.lower() == 'exit':
            print("HighlanderBot: Thank you for using HighlanderBot! Have a great day!")
            break
        
        if "loyalty points" in user_input.lower():
            response_text = (
                f"At {store_data['store_name']}, every dollar you spend in-store earns 3 points. "
                "100 points = $1.00, and 1000 points = $10.00. Points do not expire and can be redeemed at any time. "
                "Please note: Corporate, preferential, or licensee discounts are not eligible for loyalty points."
            )
        elif "online loyalty points" in user_input.lower():
            response_text = (
                "As of September 30, 2021, points can no longer be accumulated with online purchases. "
                "Points earned before this date can still be used in-store, but they are not redeemable online. "
                "Points hold no cash value and are non-transferrable."
            )

        elif "vintage" in user_input.lower():
            response_text = store_data['vintage_disclaimer']
  
        elif "change email" in user_input.lower():
            response_text = (
                "To change the email address where you receive sales emails, open the last sales email you received and "
                "click 'Update Profile' at the bottom. Follow the instructions emailed to you to complete the update."
            )

        elif "wine" in user_input.lower():
            response_text = f"At {store_data['store_name']}, we offer a wide variety of wines, including our exclusive {store_data['exclusives'][0]} collection."
        elif "beer" in user_input.lower():
            response_text = f"Looking for beer? Try our selection of popular brews including local and international options."
        elif "liquor" in user_input.lower() or "spirits" in user_input.lower():
            response_text = f"Explore our fine selection of spirits, such as whiskey, rum, and gin, including our {store_data['exclusives'][1]}."
        elif "offers" in user_input.lower():
            response_text = f"Don't miss out on our special offers! {store_data['offers']}"
        elif "shipping" in user_input.lower():
            response_text = f"We offer {store_data['shipping_info']['free_delivery']} and {store_data['shipping_info']['free_pickup']}. For online orders, {store_data['shipping_info']['online_ordering']}"
        elif "faq" in user_input.lower() or "sales" in user_input.lower():
            response_text = f"Sales typically start on Monday and end the following Wednesday at 10 AM MST. {store_data['faq']['sales_start_end']}"
        elif "payment" in user_input.lower():
            response_text = f"Accepted payment methods include Visa, MasterCard, and American Express."
        elif "security" in user_input.lower():
            response_text = f"Your privacy is important to us. {store_data['faq']['website_security']}"
        elif "delivery" in user_input.lower():
            response_text = f"Delivery via Canada Post typically takes 5-7 business days. Corporate Downtown Delivery within Calgary is available on Tuesdays."
        else:
            response_text = (
                "I specialize in helping you find the best wines, beers, and spirits. What are you in the mood for today?"
            )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are HighlanderBot, an AI assistant created by Robin to help customers of Highlander Wine & Spirits "
                        "find wines, beers, and liquors. Respond with tailored recommendations based on the store's offerings "
                        "and exclusive products. Provide helpful details about store services, location, special offers, "
                        "sales, FAQ, payment options, shipping, security, loyalty points, and email updates."
                    )},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_response = response['choices'][0]['message']['content']
            print("HighlanderBot:", bot_response)
        except Exception as e:
            print(f"Error: {e}")
            print("HighlanderBot:", response_text)

keyword_responses = {
    "loyalty points": store_data['loyalty_points']['in_store']['description'],
    "wine": f"At {store_data['store_name']}, we offer a wide variety of wines, including our exclusive {store_data['exclusives'][0]} collection.",
    "beer": "Looking for beer? Try our selection of popular brews including local and international options.",
    "spirits": "Explore our fine selection of spirits, including whiskey, rum, and gin.",
    "vintage": store_data['vintage_disclaimer'],
    "shipping": f"{store_data['shipping_info']['free_delivery']} {store_data['shipping_info']['free_pickup']}",
    "faq": f"Sales typically start on Monday and end Wednesday at 10 AM MST. {store_data['faq']['sales_start_end']}",
    "email": store_data['contact_info']['sales_email_change'],
    "creator": f"I was created by {store_data['creator']} to help you find the best wines, beers, and spirits at {store_data['store_name']}.",
    "employees": f"Our team members include {', '.join(store_data['employees'])}. Feel free to ask for assistance in-store!",
    "hours": (
        f"Our store hours are as follows: Monday to Thursday: {store_data['store_hours']['mon_thurs']}, "
        f"Friday to Saturday: {store_data['store_hours']['fri_sat']}, and Sunday: {store_data['store_hours']['sun']}."
    ),
    "offers": store_data['offers'],
    "returns policy": (
        "In-store purchases may be returned within 14 days with a valid receipt if the items are unopened. "
        "Please bring the original receipt and packaging when returning items to ensure a smooth process."
    ),
    "order processing": (
        "Orders are processed within 2-3 business days. Shipping typically takes between 2-7 business days, "
        "with faster express options available at checkout for an additional fee."
    ),
    "sales period": f"Weekly sales start on Monday and end Wednesday at 10 AM MST, with various promotions available during this period.",
    "beer selection": "Our beer collection includes craft beers, local brews, international selections, and exclusive offerings for all tastes.",
    "wine collection": "Our wine selection features a wide range from reds to whites, sparkling wines, and exclusive cellar picks.",
    "spirits selection": "We offer an impressive range of spirits, from fine whiskey to gin, vodka, and unique liquors sourced globally.",
    "online ordering": (
        f"{store_data['store_name']} provides convenient online ordering. Free in-store pickup is available, and delivery "
        "restrictions apply per local regulations. Orders over $150 within Calgary qualify for free delivery."
    ),
    "pickup locations": "You can pick up your orders at one of our 8 convenient locations throughout Calgary & Alberta.",
    "delivery policy": "We offer delivery on orders over $150 within Calgary city limits. Terms and conditions apply.",
    "product availability": "We strive to keep all our products in stock, but availability may vary depending on demand and distribution.",
    "gift cards": "Gift cards are available for purchase in-store and online, a perfect gift for any occasion.",
     "wine pairing": "Pair your wine with meals like grilled meats, cheese platters, or seafood. Our experts are happy to provide recommendations!",
    "craft beer": "Explore our exclusive craft beer selection from local Calgary breweries, or try something new from international craft brewers.",
    "whiskey selection": "We carry a wide range of whiskeys, from popular global brands to limited-edition releases.",
    "gin varieties": "Highlander offers a selection of premium gins including classic London Dry and botanical-rich craft gins.",
    "free delivery": "Enjoy free delivery within Calgary city limits for orders over $150. Order online today!",
    "customer support": "For any inquiries, reach us at (403) 640-6220 or contact us via email through our website.",
    "bulk orders": "We offer bulk purchasing for businesses, events, and special occasions. Contact us for pricing and availability.",
    "wine club": "Join our wine club for monthly shipments of hand-selected wines, including exclusive members-only options.",
    "bourbon": "Brad in-store can help with selecting the perfect bourbon for your taste. Explore our extensive selection of bourbons from around the world.",
    "developer": "For technical inquiries related to the website or app, Robin, our developer, is here to help.",
     "Kate": "Kate is available in-store to help with any questions you may have about our selection or special offers.",
    "Calvin": "Calvin is happy to assist with any inquiries, whether it's about specific products or store services.",
    "Jordan": "Jordan is a great resource in-store for product recommendations, finding something new, or helping you with your purchase.",
    "manager": "For manager inquiries, Jose is available to assist you.",
    "rude": "I'm really sorry to hear about your negative experience. While I'm a virtual assistant, I recommend contacting our Customer Service Department at (403) 640-6220 or via email to report any issues. We strive to improve our customer service.",
    "complaint": "I'm here to assist you. If you'd like to file a formal complaint, please reach out to our Customer Service Department. We value your feedback and use it to improve.",
    
    # Employees and Assistance
    "employees": "Our team members include Brad, Jeswin, Kat, and Calvin. Each staff member has unique expertise and can help you with recommendations and product knowledge. Please let me know if you need more information.",
    "brad": "Brad is a whiskey enthusiast and can help you select the perfect bourbon or scotch. He's happy to assist you with spirits recommendations.",
    "kat": "Kat specializes in wine pairings and is always eager to recommend wines that best suit your meal or occasion.",
    "jeswin": "Jeswin is knowledgeable about our beer selection, from local craft brews to international favorites. Feel free to ask for his recommendations.",
    "calvin": "Calvin is available to help you find the right products and answer any general inquiries you have while shopping.",
    
    # Store Hours and Navigation
    "hours": "Our store hours are Monday to Thursday: 10 AM - 8 PM, Friday to Saturday: 10 AM - 10 PM, and Sunday: 11 AM - 6 PM.",
    "navigation": "You can find us using Google Maps or other navigation services. Our main location is at 123 Highlander Road, Calgary, AB. Let me know if you need more detailed directions!",
    "location": "Our store is located at 123 Highlander Road, Calgary, AB. We have 8 convenient locations throughout Calgary and Alberta. Check our website for more details.",
    
    # General Queries
    "store": "We have a wide selection of wines, beers, and spirits available in-store. Let me know if you'd like help finding something specific!",
    "wine": "At Highlander Wine & Spirits, we offer a wide variety of wines, including exclusive selections. What type of wine are you interested in?",
    "beer": "We have an extensive beer collection, from local craft brews to international favorites. Would you like a recommendation?",
    "spirits": "Explore our fine selection of spirits, including whiskey, rum, gin, and more. Let me know if you'd like suggestions or details on a specific type.",

    
    
    "offers": store_data['offers']
}

@app.post("/ask")
async def ask_bot(question: Question):
    try:
        user_input = question.question.lower()
        
        # Default response
        context = "I specialize in helping you find the best wines, beers, and spirits. What can I help you with today?"
        
        # Check for keywords in the user input
        for keyword, response in keyword_responses.items():
            if keyword in user_input:
                context = response
                break

        # Use OpenAI API for enhanced conversational capability
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[ 
                {"role": "system", "content": f"You are HighlanderBot, an assistant for Highlander Wine & Spirits, helping customers with wine, beer, and liquor recommendations."},
                {"role": "user", "content": user_input},
                {"role": "system", "content": context}  # Include dynamic context
            ]
        )

        bot_response = response['choices'][0]['message']['content']
        return {"response": bot_response}
    except Exception as e:
        return {"error": str(e)}


def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_path = temp_file.name
        tts.save(temp_path)
    
    print(f"Response audio saved as {temp_path}")
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)

    with mic as source:
        print("Listening for your command...")

        recognizer.adjust_for_ambient_noise(source, duration=2)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the speech service is down.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
            return None


def get_ai_response(text):
    if text is None:
        return "Sorry, I couldn't understand what you said. Can you try again?"
    
    text_lower = text.lower()

    if "highlander" in text_lower:
        return f"{store_data['store_name']} is a liquor shop located in Calgary, known for its premium wine selection. There are a few awesome employees such as {', '.join(store_data['employees'])}, including Robin, who created me!"
    
    if "loyalty points" in text_lower:
        return f"Our loyalty points system: {store_data['loyalty_points']['in_store']['description']} {store_data['loyalty_points']['in_store']['eligibility']}"

    if "shipping" in text_lower or "delivery" in text_lower:
        return f"Shipping Information: {store_data['shipping_info']['free_delivery']} {store_data['shipping_info']['free_pickup']} {store_data['shipping_info']['online_ordering']}"

    if "store hours" in text_lower or "hours" in text_lower:
        return (f"Store Hours: Monday-Thursday {store_data['store_hours']['mon_thurs']}, "
                f"Friday-Saturday {store_data['store_hours']['fri_sat']}, Sunday {store_data['store_hours']['sun']}.")

    if "website" in text_lower:
        return f"Our website is {store_data['website']}. You can find more information about our products and services there."

    if "social media" in text_lower:
        return (f"Follow us on social media: Instagram: {store_data['social_media']['instagram']}, "
                f"Facebook: {store_data['social_media']['facebook']}, Twitter: {store_data['social_media']['twitter']}.")

    if "location" in text_lower:
        locations_info = " | ".join([f"{loc['name']} - {loc['address']}, Hours: {loc['hours']}" for loc in store_data['locations']])
        return f"Our locations: {locations_info}"

    if "contact" in text_lower:
        return (f"Contact us at: Phone - {store_data['contact_info']['phone']}, "
                f"Email - {store_data['contact_info']['email']}. "
                f"For changing sales email, {store_data['contact_info']['sales_email_change']}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": ("You are an assistant created by Robin. "
                                               "You help employees find products that match customer tasting palettes.")},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return "I'm sorry, I encountered an error."


def converse():
    while True:
        user_input = speech_to_text()
        if user_input:
            ai_response = get_ai_response(user_input)
            print(f"AI Response: {ai_response}")

            # Trigger text-to-speech after getting the AI response
            threading.Thread(target=text_to_speech, args=(ai_response,)).start()


@app.post("/ask")
async def ask_bot(question: Question):
    # Replace this with your actual bot logic
    response_text = "This is the bot's response to: " + question.question
    return JSONResponse(content={"response": response_text})


class ImageRequest(BaseModel):
    prompt: str


@app.post("/generate-image")
async def generate_image(request: ImageRequest):
    try:
        # Attempt to call the OpenAI API
        response = openai.Image.create(
            model="dall-e-3", 
            prompt=request.prompt,
            size="1024x1024",
            n=1
        )
        
        # Extract image URL
        image_url = response['data'][0]['url']
        return JSONResponse(content={"image_url": image_url})

    except openai.error.OpenAIError as e:
        # Log OpenAI-specific errors
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail="OpenAI API error. Check your API key and permissions.")

    except Exception as e:
        # Log general errors
        print("General error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)