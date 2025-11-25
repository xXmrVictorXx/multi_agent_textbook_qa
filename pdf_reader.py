"""PDF文本提取模块"""
import PyPDF2
from typing import List
import os


class PDFReader:
    """PDF文档读取器"""
    
    def __init__(self, pdf_path: str):
        """
        初始化PDF读取器
        
        Args:
            pdf_path: PDF文件路径
        """
        self.pdf_path = pdf_path
        self.text = ""
        self.pages = []
        
    def extract_text(self, max_pages: int = None) -> str:
        """
        提取PDF中的文本
        
        Args:
            max_pages: 最大提取页数，None表示提取所有页面
            
        Returns:
            提取的文本内容
        """
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {self.pdf_path}")
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                # 确定要提取的页数
                pages_to_extract = min(max_pages, total_pages) if max_pages else total_pages
                
                print(f"PDF总页数: {total_pages}")
                print(f"提取页数: {pages_to_extract}")
                
                # 逐页提取文本
                for page_num in range(pages_to_extract):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    self.pages.append(page_text)
                    self.text += page_text + "\n\n"
                    
                    if (page_num + 1) % 10 == 0:
                        print(f"已提取 {page_num + 1} 页...")
                
                print(f"文本提取完成，共提取 {len(self.text)} 个字符")
                return self.text
                
        except Exception as e:
            raise Exception(f"读取PDF文件时出错: {str(e)}")
    
    def get_page_text(self, page_num: int) -> str:
        """
        获取指定页面的文本
        
        Args:
            page_num: 页码（从0开始）
            
        Returns:
            页面文本内容
        """
        if 0 <= page_num < len(self.pages):
            return self.pages[page_num]
        return ""
    
    def get_text_summary(self, max_chars: int = 5000) -> str:
        """
        获取文本摘要（用于知识库）
        
        Args:
            max_chars: 最大字符数
            
        Returns:
            文本摘要
        """
        if len(self.text) <= max_chars:
            return self.text
        
        # 截取前N个字符
        return self.text[:max_chars] + "\n...\n（文本已截断）"


def load_pdf_knowledge(pdf_path: str, max_pages: int = None) -> str:
    """
    加载PDF知识库
    
    Args:
        pdf_path: PDF文件路径
        max_pages: 最大页数
        
    Returns:
        提取的文本内容
    """
    reader = PDFReader(pdf_path)
    return reader.extract_text(max_pages=max_pages)


if __name__ == "__main__":
    # 测试PDF读取
    pdf_path = "data/nndl-book.pdf"
    reader = PDFReader(pdf_path)
    text = reader.extract_text(max_pages=5)  # 测试时只读取前5页
    print("\n提取的文本预览:")
    print(text[:500])

