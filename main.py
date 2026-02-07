import os 
import json
from groq import Groq
from rich.console import Console
from rich.panel import Panel
from rich.table import Table  # Added for the gimmick
from dotenv import load_dotenv

load_dotenv()

apikey = os.getenv("apikey")

client = Groq(api_key=apikey)
console = Console()

def generate(userInput):
    systemInstructions = (
        "You are a LinkedIn Viral growth Bot. Your job is to take a mundane user event "
        "and transform it into a high engagement 'Bro-etry' post. "
        "Rules: \n"
        "1. Every sentence must be punchy, add three sentences at least.\n"
        "2. Turn failures into pivotal leadership moments.\n"
        "3. You must only output a JSON object with these keys: "
        "'hook', 'transformation_story', 'businesslesson', 'cringe_rating', 'hashtags'."
    )
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": systemInstructions},
            {"role": "user", "content": f"The event: {userInput}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def run_app():
    console.print("[bold cyan] LinkedIn CRINGE Generator [/bold cyan]")
    userThought = console.input("\n[bold green]What happened today?[/bold green]: ")
    
    with console.status("[bold yellow]Extracting 'thought leadership'....[/bold yellow]"):
        data = generate(userThought)

    linkedin_post = f"[bold white]{data['hook']}[/bold white]\n\n"
    
   
    sentences = [s.strip() for s in data['transformation_story'].split(".") if s.strip()]
    linkedin_post += "\n\n".join(sentences) + "\n\n"
    
    linkedin_post += f"[bold yellow]Lesson: {data['businesslesson']}[/bold yellow]\n\n"
    linkedin_post += f"[blue]{' '.join(data['hashtags'])}[/blue]\n\n"
    linkedin_post += "[italic]Agree??[/italic]"

    console.print("\n")
    console.print(Panel(linkedin_post, title="The Viral Masterpiece", border_style="blue"))


    table = Table(title="Cringe Analytics")
    table.add_column("Metric", style="magenta")
    table.add_column("Value", style="green")
    
   
    cringe_val = data.get('cringe_rating', '99')
    table.add_row("Cringe Rating", f"[red]{cringe_val}%[/red]")
    table.add_row("Self-Importance", "Maximum")
    
    console.print(table)

if __name__ == "__main__":
    run_app()