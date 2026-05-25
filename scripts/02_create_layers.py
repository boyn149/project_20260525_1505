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

    # 2. Parse details.md for book codes
    details_path = Path("book/details.md")
    with open(details_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    book_codes = re.findall(r'bookcode:\s*(book\d+)', content)
    print(f"Found book codes: {book_codes}")

    # 3. Create client
    async with await NotebookLMClient.from_storage() as client:
        conversation_id = None
        
        # 4. Generate Layers 1 to 4
        for layer_num in range(1, 5):
            print(f"--- Generating Layer {layer_num} ---")
            for book_code in book_codes:
                prompt = f"layer{layer_num} {book_code} ไม่ใช้สำนวน esther และใช้ชื่อหนังสือตามใน details.md"
                print(f"Sending prompt for {book_code}: '{prompt}'...")
                
                result = await client.chat.ask(
                    nb_id, 
                    prompt, 
                    conversation_id=conversation_id
                )
                
                # Update conversation_id to maintain session
                if conversation_id is None:
                    conversation_id = result.conversation_id
                
                answer = result.answer
                # Clean citations
                clean_answer = re.sub(r'\[\d+[^\]]*\]', '', answer)
                
                # Create book directory
                book_dir = Path(f"book/book_{book_code}")
                os.makedirs(book_dir, exist_ok=True)
                
                # Save layer file
                layer_file = book_dir / f"layer{layer_num}.md"
                with open(layer_file, "w", encoding="utf-8") as f:
                    f.write(clean_answer)
                print(f"  Saved to {layer_file}")

        print("Phase 1 complete.")

if __name__ == "__main__":
    asyncio.run(main())
