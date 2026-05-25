import asyncio
import os
from datetime import datetime
from pathlib import Path
from notebooklm import NotebookLMClient, ChatGoal

async def main():
    # 1. Create client
    async with await NotebookLMClient.from_storage() as client:
        # 2. Create a new notebook
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        notebook_title = f"project_{current_time}"
        print(f"Creating notebook: {notebook_title}")
        nb = await client.notebooks.create(notebook_title)
        nb_id = nb.id
        print(f"Notebook ID: {nb_id}")

        # 3. Add sources
        sources_to_add = [
            Path("notebooklm/context.md"),
            Path("notebooklm/project.md")
        ]
        
        # Add all files in src/
        src_dir = Path("src")
        for file_path in src_dir.iterdir():
            if file_path.is_file():
                sources_to_add.append(file_path)
        
        print(f"Adding {len(sources_to_add)} sources...")
        for source_path in sources_to_add:
            print(f"  Adding {source_path.name}...")
            await client.sources.add_file(nb_id, source_path)
        
        # 4. Inject instruction.md into Configure Chat
        instruction_path = Path("notebooklm/instruction.md")
        with open(instruction_path, "r", encoding="utf-8") as f:
            instruction_content = f.read()
        
        print("Configuring chat with instruction.md...")
        await client.chat.configure(
            nb_id,
            goal=ChatGoal.CUSTOM,
            custom_prompt=instruction_content
        )
        
        # 5. Send prompt: "details โดยอ้างอิงจาก project.md"
        print("Sending prompt: 'details โดยอ้างอิงจาก project.md'...")
        result = await client.chat.ask(nb_id, "details โดยอ้างอิงจาก project.md")
        answer = result.answer
        
        # 6. Save answer in book/details.md
        # Strip citations if any (Global Rule 6)
        import re
        clean_answer = re.sub(r'\[\d+[^\]]*\]', '', answer)
        
        os.makedirs("book", exist_ok=True)
        details_path = Path("book/details.md")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(clean_answer)
        print(f"Saved answer to {details_path}")
        
        # 7. Add details.md to sources
        print("Adding details.md to sources...")
        await client.sources.add_file(nb_id, details_path)
        
        print("Phase 0 complete.")
        # Store notebook ID for next phases
        with open("current_notebook_id.txt", "w") as f:
            f.write(nb_id)

if __name__ == "__main__":
    asyncio.run(main())
