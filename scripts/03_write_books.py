import asyncio
import os
import re
from pathlib import Path
from notebooklm import NotebookLMClient

async def main():
    # 1. Load notebook ID
    if not os.path.exists("current_notebook_id.txt"):
        print("Error: current_notebook_id.txt not found.")
        return
    with open("current_notebook_id.txt", "r") as f:
        nb_id = f.read().strip()

    # 2. Parse details.md for books
    details_path = Path("book/details.md")
    with open(details_path, "r", encoding="utf-8") as f:
        details_content = f.read()
    
    # regex to get book_code and book_name
    books = re.findall(r'# bookcode:\s*(book\d+)\n# book_name:\s*(.+)', details_content)
    print(f"Found books: {books}")

    async with await NotebookLMClient.from_storage() as client:
        for book_code, book_name in books:
            print(f"--- Processing {book_code}: {book_name} ---")
            
            # a. Source Management: Remove other books' layers
            sources = await client.sources.list(nb_id)
            for src in sources:
                # Check if it's a layer file and NOT for the current book
                if src.title and "layer" in src.title and book_code not in src.title:
                    print(f"  Removing source: {src.title} ({src.id})")
                    await client.sources.delete(nb_id, src.id)
            
            # b. Add current book's layers
            book_dir = Path(f"book/book_{book_code}")
            for i in range(1, 5):
                layer_path = book_dir / f"layer{i}.md"
                if layer_path.exists():
                    print(f"  Adding source: {layer_path}")
                    await client.sources.add_file(nb_id, layer_path)
            
            # c. Prepare book file
            # Clean book name for filename (Rule Phase 2: ระวังเครื่องหมายที่ Windows ใช้ตั้งชื่อไม่ได้)
            clean_name = re.sub(r'[<>:"/\\|?*]', '_', book_name).replace(' ', '_')
            output_file = book_dir / f"book_{book_code}_{clean_name}.md"
            
            # Clear file if exists
            with open(output_file, "w", encoding="utf-8") as f:
                pass
            
            # d. Prompts sequence
            # We need to know con-a-b-c from layer3.md
            layer3_path = book_dir / "layer3.md"
            with open(layer3_path, "r", encoding="utf-8") as f:
                l3_content = f.read()
            
            # Simple heuristic for con-a-b-c based on "หัวข้อ X.Y"
            topics = re.findall(r'หัวข้อ\s*(\d+)\.(\d+)', l3_content)
            # Assume section 1 if not specified
            prompts = ["preface"]
            for ch, top in topics:
                prompts.append(f"con-1-{ch}-{top} ใช้หัวข้อตาม outline ใน layer3.md")
            prompts.extend(["reference", "bio", "contact"])
            
            # e. Execute prompts
            for prompt in prompts:
                print(f"  Sending prompt: {prompt}")
                # Use new conversation_id for each prompt (Rule Phase 2: แบบ conversation prompting แยกบท)
                result = await client.chat.ask(nb_id, prompt)
                answer = result.answer
                
                # Strip citations (Global Rule 6)
                clean_answer = re.sub(r'\[\d+[^\]]*\]', '', answer)
                
                # Append to book file
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(clean_answer + "\n\n")
            
            print(f"  Finished {book_code}. Output: {output_file}")

        print("Phase 2 complete.")

if __name__ == "__main__":
    asyncio.run(main())
