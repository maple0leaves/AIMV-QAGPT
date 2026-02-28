import os
import fitz  # PyMuPDF
import uuid
from PIL import Image
import torch
from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
import chromadb
from chromadb.config import Settings

def load_all_pdfs_to_knowledge(pdf_dir="./batch_pdfs", collection_name="default"):
    # 初始化 ChromaDB 向量数据库
    client = chromadb.Client(Settings(
        persist_directory="./chroma_store",
        chroma_db_impl="duckdb+parquet"
    ))

    # 创建或获取知识库 collection
    try:
        collection = client.get_collection(name=collection_name)
    except:
        collection = client.create_collection(name=collection_name)

    # 加载文本嵌入模型
    print("🔠 正在加载文本嵌入模型...")
    text_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # 768维

    # 加载图像嵌入模型（CLIP）
    print("🖼️ 正在加载图像嵌入模型...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # 遍历 PDF 文件夹
    for filename in os.listdir(pdf_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_dir, filename)
        print(f"📄 正在处理：{pdf_path}")
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            # 提取文本
            text = page.get_text().strip()
            if text:
                text_vec = text_model.encode(text).tolist()
                collection.add(
                    documents=[text],
                    embeddings=[text_vec],
                    ids=[str(uuid.uuid4())],
                    metadatas=[{
                        "type": "text",
                        "source": filename,
                        "page": page_num + 1
                    }]
                )

            # 提取图像
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(fitz.open("png", image_bytes).extract_image(xref)["image"]).convert("RGB")

                inputs = clip_processor(images=image, return_tensors="pt")
                with torch.no_grad():
                    image_vec = clip_model.get_image_features(**inputs)[0].cpu().numpy().tolist()

                collection.add(
                    documents=[f"{filename} 第{page_num+1}页 图{img_index+1}"],
                    embeddings=[image_vec],
                    ids=[str(uuid.uuid4())],
                    metadatas=[{
                        "type": "image",
                        "source": filename,
                        "page": page_num + 1
                    }]
                )

    print("✅ 所有 PDF 文件（文本 + 图片）已成功写入知识库")
