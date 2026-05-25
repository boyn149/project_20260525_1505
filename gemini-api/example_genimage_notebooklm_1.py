#🎯 วิธีการทำงาน
#✅ สร้าง infographic → ได้ task_id
#✅ รอให้เสร็จด้วย wait_for_completion()
#✅ เมื่อเสร็จ → เรียก artifacts.list() เพื่อดึงรายการ artifacts
#✅ กรองเฉพาะ infographic ที่ is_completed = True
#✅ เอารูปล่าสุด (index 0) → ได้ artifact_id
#✅ ดาวน์โหลดด้วย artifact_id นั้น


import asyncio
import os
import re
import json
from pathlib import Path
from datetime import datetime
from notebooklm import NotebookLMClient, InfographicOrientation, InfographicStyle

async def generate_images():
    """
    Phase 4: สร้างรูปภาพสำหรับ book1
    1. สร้าง infographic จาก NotebookLM
    2. ดาวน์โหลดรูปภาพเก็บไว้ใน pic_book1/
    3. บันทึกผลลงใน pic_ture_details.md
    """
    
    notebook_id = "fc75cd1c-5f03-4563-9ddf-6027787b7021"
    book_code = "book1"
    output_dir = Path(f"book/book_{book_code}/pic_book1")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prompts จากไฟล์หนังสือ
    prompts = [
        {
            "id": 1,
            "prompt": "Informational Infographic showing the combination of Ni (Mystery) and Fe (Empathy) creating a powerful Passive Attraction aura for INFJ personality, aspect ratio 16:8, minimal style, white background. All text in the image must be in Thai.",
            "filename": f"infographic_{book_code}_1.png"
        },
        {
            "id": 2,
            "prompt": "Grid Infographic showing 3 elements of Passive Attraction for INFJ based on Art of Seduction: 1. The Ideal Lover (Fe empathy), 2. The Star (Ni mystery), 3. The Coquette (Space and boundary). Text must be entirely in Thai language, aspect ratio 16:8, minimal style, white background",
            "filename": f"infographic_{book_code}_2.png"
        }
    ]

    print(f"🚀 Starting Phase 4: Image Generation for {book_code}")
    print(f"📓 Notebook ID: {notebook_id}\n")
    
    # เก็บผลลัพธ์
    results = []

    async with await NotebookLMClient.from_storage() as client:
        for item in prompts:
            print(f"{'='*80}")
            print(f"🎨 Image {item['id']}/{len(prompts)}: {item['filename']}")
            print(f"{'='*80}")
            
            result_data = {
                "prompt_id": item['id'],
                "filename": item['filename'],
                "prompt": item['prompt'],
                "task_id": None,
                "artifact_id": None,
                "status": "pending",
                "output_path": None,
                "error": None
            }
            
            try:
                # สร้าง infographic
                result = await client.artifacts.generate_infographic(
                    notebook_id,
                    instructions=item['prompt'],
                    orientation=InfographicOrientation.LANDSCAPE,
                    style=InfographicStyle.PROFESSIONAL
                )
                
                # เก็บ Task ID
                task_id = result.task_id
                result_data['task_id'] = task_id
                
                print(f"✓ Started generation")
                print(f"  📋 Task ID: {task_id}")
                
                # รอให้สร้างเสร็จ
                print(f"⏳ Waiting for completion (max 10 min)...")
                final_status = await client.artifacts.wait_for_completion(
                    notebook_id,
                    task_id,
                    timeout=600,
                    initial_interval=20  # ✅ แก้ไขตาม warning
                )
                
                if final_status.is_complete:
                    print(f"✅ Generation completed!")
                    
                    # ✅ หา artifact_id จาก artifact list (เรียงตามเวลาล่าสุด)
                    print(f"🔍 Finding artifact ID...")
                    artifacts = await client.artifacts.list(notebook_id)
                    
                    # กรอง infographic ที่สร้างเสร็จ
                    infographics = [
                        a for a in artifacts 
                        if a.kind == 'infographic' and a.is_completed
                    ]
                    
                    if infographics:
                        # เอารูปล่าสุด (index 0)
                        latest_infographic = infographics[0]
                        artifact_id = latest_infographic.id
                        
                        result_data['artifact_id'] = artifact_id
                        result_data['status'] = 'completed'
                        
                        print(f"  🎨 Artifact ID: {artifact_id}")
                        
                        # ดาวน์โหลดรูปภาพ
                        output_path = output_dir / item['filename']
                        downloaded_path = await client.artifacts.download_infographic(
                            notebook_id, 
                            str(output_path), 
                            artifact_id=artifact_id
                        )
                        
                        result_data['output_path'] = str(downloaded_path)
                        
                        print(f"💾 Downloaded to: {downloaded_path}")
                    else:
                        result_data['status'] = 'error'
                        result_data['error'] = 'No infographic artifacts found'
                        print(f"❌ No infographic found")
                    
                else:
                    result_data['status'] = 'failed'
                    result_data['error'] = f"Status: {final_status.status}"
                    print(f"❌ Generation failed or timed out")
                    print(f"  Status: {final_status.status}")
            
            except Exception as e:
                result_data['status'] = 'error'
                result_data['error'] = str(e)
                print(f"❌ Error: {e}")
            
            results.append(result_data)
            print()  # Empty line
            
            # Delay ระหว่างการสร้าง
            if item['id'] < len(prompts):
                delay = 10
                print(f"⏳ Waiting {delay}s before next generation...\n")
                await asyncio.sleep(delay)
    
    # บันทึกผลลัพธ์
    print(f"{'='*80}")
    print(f"📊 Summary")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['status'] == 'completed')
    print(f"✅ Success: {success_count}/{len(results)}")
    print(f"❌ Failed: {len(results) - success_count}/{len(results)}")
    
    # บันทึกเป็น JSON
    metadata_file = output_dir / "generation_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            "book_code": book_code,
            "notebook_id": notebook_id,
            "generated_at": datetime.now().isoformat(),
            "total_images": len(results),
            "successful": success_count,
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Metadata saved to: {metadata_file}")
    
    # แสดงรายละเอียด IDs
    print(f"\n{'='*80}")
    print(f"📋 Generated IDs")
    print(f"{'='*80}")
    for r in results:
        print(f"\n{r['filename']}:")
        print(f"  Task ID:     {r['task_id']}")
        print(f"  Artifact ID: {r['artifact_id']}")
        print(f"  Status:      {r['status']}")
        if r['output_path']:
            print(f"  Path:        {r['output_path']}")
    
    print(f"\n🏁 Image generation process finished.")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(generate_images())