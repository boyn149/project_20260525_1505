# instruction-outline
## trigger command details
ให้ details = การเขียนรายละเอียดหังสือทั้งหมดตามใน project.md โดยต้องตั้งชื่อหนังสือแต่ลละเล่ม(book_name)

[output-format]
1. ไม่ต้องใช้สำนวนเอสเธอร์
2. มีรายละเอียดหังสือแต่ละเล่ม
   1. book_code
   2. book_name
   3. philosophy
   4. objective
   5. constrain

## การเรียกชื่อหนังสือ
book_code : ชื่อรหัสหนังสือที่เรียนในไฟล์ project.md เช่น book1,book2,workbook1 เป็นต้น
book_name : ชื่อหนังสือที่ notebooklm ตั้งขึ้น 

example
# bookcode: book1
# book_name: [ชื่อหนังสือ1]
# Philosophy 
{เนื้อหาเป็นบรรยาย}
# Ojective
{เนื้อหาเป็น numberlist}
# Constrain
{เนื้อหาเป็น numberlist}

# bookcode: book2
# book_name: [ชื่อหนังสือ2]
# Philosophy 
{เนื้อหาเป็นบรรยาย}
# Ojective
{เนื้อหาเป็น numberlist}
# Constrain
{เนื้อหาเป็น numberlist}

## trigger command layer
ให้ layer1 = เขียน layer1 จากข้อมูลที่ได้จาก details.md และ project.md
ให้ layer2 = เขียน layer2 จากข้อมูลที่ได้จาก details.md และ project.md
ให้ layer3 = เขียน layer3 จากข้อมูลที่ได้จาก details.md และ project.md
ให้ layer4 = เขียน layer4 จากข้อมูลที่ได้จาก details.md และ project.md

[outputformat]
1. ไม่ต้องใช้สำนวนเอสเธอร์
2. layer1-4 ให้อ้างอิงจาก book-architecture ใน context.md
3. มี title ใน format h1(#) อยู่บนสุด


# instruction-content


## trigger command
ให้ con-a-b-c = เขียนเนื้อหา โดย 
 - a คือ section(ส่วน) 
 - b คือchapter(บท) 
 - c คือ topic(หัวข้อ) 
 - เช่น con-1-2-4 หมายถึงเขียน หัวข้อที่ 1.4 ของบทที่ 2 ของส่วนที่ 1 ของ outline ใน layer3 

## step การทำงาน
1. ดูไฟล์ layer1-4 เพื่อเลือก 
   1. style จาก layer2
   2. เลือกหัวข้อจากส่วน outline ใน layer3
   3. รูปแบบการเขียน จาก layer4
2. ดูและใช้ constrain-con ใน context.md
3. เช็ค case ให้ถูกต้อง
4. เขียนเนื้อหาตามที่กำหนด 

## Recheck
1. ทวนสอบชื่อหัวข้อกับส่วน outline ใน layer3 อีกครั้งว่าถูกต้องและสอดคล้องกับเลข a-b-c ที่เรียกมา
2. ตรวจสอบเงื่อนไข Case 1-4 เพื่อให้แน่ใจว่าการแสดง Heading tag (#, ##, ###) รวมถึงการใส่ Transition logic in/out ถูกต้องตามตำแหน่งของหัวข้อนั้นๆ ในบท
3. ตรวจสอบข้อความ meta ห้ามเขียนข้อความ meta (ข้อความที่ไม่เกี่ยวกับเนื้อหา) เช่น trasition logic in, trasition logic out,RWP,RWOP



# instruction-preface
preface = เขียนคำนำของหนังสือ โดย
1. ไม่ต้องมีรูป, infographic, callout box, table
2. ใช้ข้อมูลจาก layer1 มาประกอบการเขียน
3. มี "คำนำ" เป็น h1(#) อยู่บนสุด
4. ใช้สำนวน Eshter 


# instruction-bio
ิbio = เขียน about author

# instruction-reference
reference = เขียนหนัวสืออ้างอิง

# instruction-contact
contact = เชียนช่องทางการติดต่อ

