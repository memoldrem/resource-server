from app import db
from app.repositories.forum_repository import ForumRepository
from app.repositories.thread_repository import ThreadRepository
from app.repositories.post_repository import PostRepository
from faker import Faker
from datetime import datetime, timedelta
import pytz
from app import create_app

fake = Faker()

FORUM_CATEGORIES = [
    # Technology & Innovation
    "Blockchain & Cryptocurrency", "AI & Machine Learning", "Cybersecurity", "Software Development", 
    "Cloud Computing", "Virtual Reality & Augmented Reality", "Data Science & Big Data", "Robotics", 
    "Quantum Computing", "Web Development", "Mobile Development", "Tech News & Trends", "Startups & Entrepreneurship",

    # Business & Economy
    "Entrepreneurship", "Financial Technology (FinTech)", "Marketing & Advertising", "E-Commerce & Retail", 
    "Investing & Stock Market", "Leadership & Management", "Productivity & Time Management", 
    "Sales Strategies", "Small Business Tips", "Corporate Social Responsibility", "Sustainability in Business", 
    "Business Analytics", "Real Estate", "Corporate Finance",

    # Health & Wellness
    "Mental Health & Wellbeing", "Fitness & Nutrition", "Healthy Living", "Medical Technology", "Biohacking", 
    "Telemedicine", "Personalized Medicine", "Healthcare Policy", "Wellness Lifestyle", "Public Health",
    "Fitness Challenges", "Self-care Routines", "Medical Research", "Health Innovations",

    # Environment & Sustainability
    "Climate Change", "Sustainable Living", "Renewable Energy", "Zero Waste Lifestyle", "Green Building", 
    "Sustainable Fashion", "Environmental Advocacy", "Eco-Friendly Technology", "Nature & Wildlife", "Urban Sustainability", 
    "Clean Water & Sanitation", "Plastic-Free Movement", "Food Security & Agriculture", "Green Finance",

    # Social Issues & Ethics
    "Human Rights", "Diversity & Inclusion", "Equality & Social Justice", "Gender Equality", 
    "Racial Justice", "Digital Privacy & Security", "Corporate Ethics", "Civil Rights & Liberties", 
    "Volunteering & Social Impact", "Ethical Business Practices", "Social Responsibility", "Ethical Technology", 
    "LGBTQ+ Rights", "Disability Advocacy", "Refugee Rights",

    # Science & Space
    "Space Exploration", "Astronomy & Astrophysics", "Climate Science", "Physics & Engineering", 
    "Genetics & Biotechnology", "Neuroscience", "Marine Biology", "Geology & Earth Sciences", "Ecology & Conservation",
    "Space Missions & Satellites", "Scientific Research & Innovation", "Exoplanets & Habitable Worlds", 
    "Artificial Intelligence in Science", "Futuristic Technologies",

    # Arts, Culture & Entertainment
    "Art & Design", "Film & Movies", "Music & Audio Production", "Photography", "Performing Arts", 
    "Literature & Writing", "Cultural Heritage & Preservation", "Virtual Art & NFTs", "Games & Interactive Media", 
    "Fashion & Style", "Photography & Visual Arts", "Art Exhibitions", "Crafts & DIY", "Pop Culture", 
    "Celebrity News", "Television Shows", "Theater & Drama",

    # Travel & Adventure
    "Travel Tips & Guides", "Adventure Sports", "Solo Travel", "Sustainable Tourism", "Travel Photography", 
    "Backpacking", "Cultural Exploration", "Budget Travel", "Luxury Travel", "Travel Hacks", 
    "Adventure Destinations", "Travel Safety & Health", "Digital Nomad Life", "Road Trips",

    # Education & Learning
    "Online Learning & MOOCs", "Career Development", "Study Tips", "College Life", "Graduate Programs",
    "Certifications & Courses", "Learning Technologies", "Language Learning", "Coding Bootcamps", 
    "Entrepreneurship Education", "STEM Fields", "Soft Skills Development", "Public Speaking", 
    "Productivity for Students", "Mentorship & Networking",

    # Food & Drink
    "Recipes & Cooking Tips", "Healthy Eating", "Food Trends", "Restaurant Reviews", "Beverages & Cocktails", 
    "Sustainable Eating", "Vegan & Vegetarian", "Food Photography", "Food Culture & History", "Street Food", 
    "Home Brewing", "Culinary Arts", "Gastronomy", "International Cuisines", "Baking",

    # Sports & Fitness
    "Team Sports", "Individual Sports", "Fitness Goals", "Sports Training", "Nutrition for Athletes", 
    "Mental Toughness", "Outdoor Adventures", "Yoga & Meditation", "CrossFit", "Sports Psychology",
    "Cycling", "Running & Marathon", "Swimming", "Weight Training", "Sports News & Events",
]
THREAD_TEMPLATES = [
    "What are your thoughts on {buzzword} in {category}?",
    "How will {buzzword} change the future of {category}?",
    "The role of {buzzword} in {category}: A detailed discussion.",
    "Is {buzzword} the key to success in {category}?",
    "Challenges and opportunities of {buzzword} in {category}.",
    "What are the latest trends in {category}? Discuss {buzzword}.",
    "How can {category} leverage {buzzword} for growth?",
    "Why {buzzword} is crucial for the {category} industry.",
    "The impact of {buzzword} on {category} in the next decade.",
    "Do you think {buzzword} will dominate {category} in the coming years?",
    "Is {buzzword} just a trend in {category}, or is it here to stay?",
    "The ethical considerations of using {buzzword} in {category}.",
    "Exploring the future of {category} with {buzzword}.",
    "What are the most pressing issues in {category} related to {buzzword}?",
    "Can {buzzword} revolutionize the way we approach {category}?",
    "What are the biggest challenges to implementing {buzzword} in {category}?",
    "How can {category} adapt to the rapid growth of {buzzword}?",
    "A deep dive into how {buzzword} is shaping {category}.",
    "The benefits of {buzzword} in {category}: What you need to know.",
    "Debate: Will {buzzword} improve or harm {category}?",
    "What are the risks of integrating {buzzword} into {category}?"
]
BUZZWORDS = [
    # Technology & Innovation
    "blockchain", "quantum computing", "artificial intelligence", "machine learning", "cybersecurity",
    "edge computing", "5G", "cloud computing", "metaverse", "augmented reality", "virtual reality",
    "robotics", "internet of things (IoT)", "smart cities", "digital transformation", "natural language processing",
    "data science", "autonomous systems", "neural networks", "chatbots", "computer vision",

    # Business & Economy
    "entrepreneurship", "startup culture", "business intelligence", "digital marketing", "supply chain optimization",
    "consumer behavior", "customer experience", "brand loyalty", "market disruption", "corporate innovation",
    "growth hacking", "financial technology (fintech)", "leadership", "remote work", "corporate social responsibility",

    # Health & Wellness
    "mental health", "telemedicine", "genomics", "biohacking", "healthcare innovation", "personalized medicine",
    "health tech", "wellness culture", "fitness tracking", "nutraceuticals", "epigenetics", "crisis care",
    "health data", "preventive healthcare", "remote patient monitoring", "health optimization",

    # Environmental Sustainability
    "climate change", "green energy", "renewable resources", "carbon footprint", "sustainability",
    "clean energy", "circular economy", "greenwashing", "carbon neutral", "biodiversity conservation",
    "eco-friendly", "sustainable agriculture", "environmental impact", "zero waste", "energy efficiency",

    # Social Issues & Ethics
    "social justice", "equality", "human rights", "diversity and inclusion", "gender equality",
    "racial equity", "fair trade", "ethical sourcing", "corporate responsibility", "privacy rights",
    "transparency", "accountability", "digital ethics", "social impact", "freedom of speech",

    # Science & Space
    "space exploration", "astronomy", "space travel", "space tourism", "exoplanets", "dark matter", 
    "astrobiology", "scientific innovation", "bioengineering", "gene editing", "climate science", "neuroscience",
    "physics", "quantum mechanics", "space missions", "technological singularity",

    # Arts & Culture
    "digital art", "NFTs", "creativity", "augmented reality art", "artificial intelligence in art", "creative coding",
    "design thinking", "cultural heritage", "interactive media", "globalization", "urban culture", "alternative music",
    "performance art", "art activism", "street art", "virtual performances"
]


def generate_fake_forum():
    forum_category = fake.random_element(FORUM_CATEGORIES)
    forum_name = f"{forum_category} Forum"
    description = f"A forum about {forum_category} and related topics."
    forum = ForumRepository.create_forum(forum_name, description)
    return forum

def generate_fake_thread(forum):
    thread_template = fake.random_element(THREAD_TEMPLATES)
    buzzword = fake.random_element(BUZZWORDS)
    category = fake.random_element(FORUM_CATEGORIES)
    thread_title = thread_template.format(buzzword=buzzword, category=category)

    thread = ThreadRepository.create_thread(thread_title, forum.id, 1)
    return thread

def generate_fake_post(thread):
    # Select a random template and replace placeholders with random buzzwords and categories
    post_template = fake.random_element(THREAD_TEMPLATES)
    buzzword = fake.random_element(BUZZWORDS)
    category = fake.random_element(FORUM_CATEGORIES)
    post_content = post_template.format(buzzword=buzzword, category=category)

    # Use random timestamps within a reasonable range
    time_difference = fake.random_int(min=1, max=1000)
    created_at = datetime.now(pytz.UTC) - timedelta(minutes=time_difference)
    updated_at = created_at + timedelta(minutes=fake.random_int(min=1, max=30))  # Posts are updated within a short time after creation
    
    post = PostRepository.create_post(
        content=post_content, 
        thread_id=thread.id, 
        author_id=1,
    )
    return post

def generate_fake_data(num_forums=5, threads_per_forum=3, posts_per_thread=10):
    for _ in range(num_forums):
        forum = generate_fake_forum()  # Create a forum
        for _ in range(threads_per_forum):
            thread = generate_fake_thread(forum)  # Create a thread for the forum
            for _ in range(posts_per_thread):
                generate_fake_post(thread)  # Create posts within the thread

    print(f"Generated {num_forums} forums with {threads_per_forum} threads each, and {posts_per_thread} posts per thread.")

if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    with app.app_context():  # Ensure app context is active
        generate_fake_data()
