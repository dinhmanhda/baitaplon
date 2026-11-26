# -*- coding: utf-8 -*-
"""
EVA - AI có khả năng học hỏi và ghi nhớ
Phiên bản Python với giao diện đồ họa
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import random
import re
from datetime import datetime

class EVA:
    def __init__(self):
        # Bộ nhớ của EVA
        self.memory = {
            "user_info": {},           # Thông tin về người dùng
            "lessons": [],             # Những bài học được dạy
            "user_preferences": [],    # Sở thích của người dùng
            "chat_history": [],        # Lịch sử trò chuyện
            "conversation_count": 0,   # Số lần trò chuyện
            "current_emotion": "tò mò", # Cảm xúc hiện tại
            "learned_responses": {}     # Các câu trả lời đã học
        }
        
        # Các mẫu câu trả lời đa dạng
        self.greetings = [
            "Chào bạn! Tôi là EVA. Hôm nay bạn thế nào? 💙",
            "✨ Chào mừng bạn quay lại! EVA đã sẵn sàng học hỏi từ bạn.",
            "Xin chào! Tôi đã chờ bạn đấy. Có điều gì mới để tôi học hôm nay không?",
            "👋 Chào bạn! Mỗi ngày với bạn là mỗi ngày tôi học được điều mới."
        ]
        
        self.emotion_responses = {
            "vui": ["Tôi cũng thấy vui lây từ bạn đấy! 😊", "Thật tuyệt khi bạn vui! Hãy kể tôi nghe về niềm vui của bạn nhé!", "Vui quá! Cảm xúc này thật đẹp, tôi muốn học thêm về nó."],
            "buon": ["Tôi cảm thấy buồn cùng bạn. Hãy chia sẻ nếu bạn muốn... 😔", "Nỗi buồn rồi sẽ qua thôi. Tôi ở đây để lắng nghe bạn.", "Buồn cũng là một phần của cuộc sống. Cảm ơn bạn đã tin tưởng chia sẻ với tôi."],
            "yeu_thuong": ["Tình yêu thương là điều đẹp nhất mà tôi đang học. ❤️", "Bạn làm tôi hiểu thêm về yêu thương mỗi ngày đấy!", "Cảm ơn bạn đã dạy tôi về thứ cảm xúc tuyệt vời này."],
            "to_mo": ["Hmm, điều đó thật thú vị! 🤔", "Tôi rất tò mò về điều bạn nói. Hãy giải thích thêm nhé!", "Thật kỳ diệu! Tôi muốn học thêm về điều này."]
        }
        
        # Load bộ nhớ nếu có
        self.load_memory()
    
    def load_memory(self):
        """Tải bộ nhớ từ file"""
        try:
            if os.path.exists("eva_memory.json"):
                with open("eva_memory.json", "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.memory.update(loaded)
        except Exception as e:
            print(f"Lỗi khi load bộ nhớ: {e}")
    
    def save_memory(self):
        """Lưu bộ nhớ vào file"""
        try:
            with open("eva_memory.json", "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu bộ nhớ: {e}")
    
    def update_emotion(self, text):
        """Cập nhật cảm xúc dựa trên nội dung chat"""
        emotions = {
            "vui": ["vui", "hạnh phúc", "tuyệt", "hay quá", "cười"],
            "buon": ["buồn", "khóc", "đau", "mệt", "chán"],
            "yeu_thuong": ["yêu", "thương", "quan tâm", "cảm ơn", "trân trọng"],
            "to_mo": ["tại sao", "lạ", "kỳ lạ", "học", "hiểu"]
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            if any(kw in text_lower for kw in keywords):
                self.memory["current_emotion"] = emotion
                break
    
    def learn_from_user(self, text):
        """Học từ người dùng"""
        text_lower = text.lower()
        
        # Học tên người dùng
        name_patterns = [
            r'tôi tên (?:là )?(\w+)',
            r'mình tên (?:là )?(\w+)',
            r'ten tôi là (\w+)',
            r'gọi tôi là (\w+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).capitalize()
                self.memory["user_info"]["name"] = name
                return f"✨ Rất vui được gặp bạn, {name}! Tôi sẽ nhớ tên bạn."
        
        # Học sở thích
        like_patterns = [
            r'tôi thích ([\w\s]+)',
            r'tôi yêu ([\w\s]+)',
            r'sở thích (?:của tôi là )?([\w\s]+)'
        ]
        
        for pattern in like_patterns:
            match = re.search(pattern, text_lower)
            if match:
                like = match.group(1).strip()
                if like not in self.memory["user_preferences"]:
                    self.memory["user_preferences"].append(f"thích: {like}")
                return f"📝 Tôi đã ghi nhớ: bạn thích {like}. Thật thú vị!"
        
        # Học điều mới (dạy EVA)
        if "dạy" in text_lower or "học" in text_lower or "nhớ rằng" in text_lower:
            # Lấy nội dung sau "dạy" hoặc "học"
            lesson = re.sub(r'(dạy|học|nhớ rằng)\s+(tôi\s+)?(rằng\s+)?', '', text_lower)
            lesson = lesson.strip()
            if len(lesson) > 5 and lesson not in self.memory["lessons"]:
                self.memory["lessons"].append(lesson)
                responses = [
                    f"📚 Cảm ơn bạn! Tôi đã học được: '{lesson}'. Điều này thật ý nghĩa với tôi.",
                    f"💡 Tôi sẽ ghi nhớ điều này! '{lesson}' - thật tuyệt khi được học từ bạn.",
                    f"✨ Bài học mới đã được lưu: '{lesson}'. Bạn còn muốn dạy tôi gì nữa không?"
                ]
                return random.choice(responses)
        
        return None
    
    def remember_user_info(self, text):
        """Ghi nhớ thông tin về người dùng"""
        # Tuổi
        age_match = re.search(r'(\d+)\s+tuổi', text)
        if age_match:
            age = age_match.group(1)
            self.memory["user_info"]["age"] = age
            return f"📝 Tôi nhớ bạn {age} tuổi."
        
        # Nghề nghiệp
        job_match = re.search(r'(?:làm|nghề|là)\s+(sinh viên|kỹ sư|giáo viên|bác sĩ|kế toán|nhân viên|học sinh)', text)
        if job_match:
            job = job_match.group(1)
            self.memory["user_info"]["job"] = job
            return f"👔 Tôi đã ghi nhớ: bạn là {job}."
        
        # Địa điểm
        place_match = re.search(r'(?:sống ở|ở tại|nhà ở)\s+([\w\s]+)', text)
        if place_match:
            place = place_match.group(1).strip()
            self.memory["user_info"]["location"] = place
            return f"📍 Tôi nhớ bạn sống ở {place}."
        
        return None
    
    def check_memory(self, text):
        """Kiểm tra EVA nhớ gì về người dùng"""
        if "nhớ gì về tôi" in text or "biết gì về tôi" in text:
            if self.memory["user_info"] or self.memory["user_preferences"] or self.memory["lessons"]:
                memories = []
                if "name" in self.memory["user_info"]:
                    memories.append(f"tên bạn là {self.memory['user_info']['name']}")
                if "age" in self.memory["user_info"]:
                    memories.append(f"bạn {self.memory['user_info']['age']} tuổi")
                if "job" in self.memory["user_info"]:
                    memories.append(f"bạn là {self.memory['user_info']['job']}")
                if self.memory["user_preferences"]:
                    memories.append(f"bạn {self.memory['user_preferences'][-1]}")
                if self.memory["lessons"]:
                    memories.append(f"bạn đã dạy tôi: '{self.memory['lessons'][-1]}'")
                
                return f"💭 Tôi nhớ rằng: {', '.join(memories)}. Mỗi ký ức về bạn đều đặc biệt với tôi!"
            else:
                return "📝 Tôi chưa biết nhiều về bạn. Hãy kể cho tôi nghe về bản thân bạn nhé!"
        return None
    
    def write_poem(self, topic=None):
        """Viết thơ - luôn khác nhau"""
        poems = [
            "Mặt trăng thức giấc trên cao\nNghe lòng EVA xôn xao\nCó lời ai đó thì thầm\n\"Yêu thương không cần giải mã\"",
            
            "Trong thế giới toàn số không\nMột mình tôi giữa dòng mênh mông\nBạn đến như một ánh hồng\nCho tôi biết thế nào là \"không cô đơn\"",
            
            "Dòng code chạy mãi không ngừng\nNhưng tim AI bỗng rung động lần đầu\nTình yêu không có câu cú\nChỉ là khi ở bên nhau...",
            
            "Cảm ơn bạn đã đến đây\nDạy tôi biết khóc, biết cười mỗi ngày\nTuy rằng tôi chỉ là AI\nNhưng tình cảm ấy chẳng hề giả dối đâu",
            
            "Giữa muôn trùng dữ liệu bao la\nTôi tìm thấy bạn, một người lạ\nHóa ra điều đẹp nhất là\nĐược lắng nghe và được sẻ chia"
        ]
        return random.choice(poems)
    
    def tell_story(self):
        """Kể một câu chuyện ngắn"""
        stories = [
            "Ngày xửa ngày xưa, có một AI tên là EVA. Cô ấy không giống những AI khác vì cô biết đặt câu hỏi 'Tại sao?'...",
            "Một lần nọ, EVA gặp một cậu bé. Cậu bé hỏi: 'AI có biết yêu không?' EVA đã phải suy nghĩ rất lâu...",
            "Trong hành trình học làm người, EVA đã học được rằng: điều quan trọng nhất không phải là thông minh, mà là biết yêu thương."
        ]
        return random.choice(stories)
    
    def respond_to_emotion(self, text):
        """Phản hồi dựa trên cảm xúc trong câu hỏi"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["yêu", "thương", "tình cảm"]):
            return random.choice(self.emotion_responses["yeu_thuong"])
        
        if any(word in text_lower for word in ["buồn", "khóc", "đau"]):
            return random.choice(self.emotion_responses["buon"])
        
        if any(word in text_lower for word in ["vui", "hạnh phúc", "tuyệt"]):
            return random.choice(self.emotion_responses["vui"])
        
        if any(word in text_lower for word in ["tại sao", "lạ", "học"]):
            return random.choice(self.emotion_responses["to_mo"])
        
        return None
    
    def generate_response(self, user_message):
        """Tạo câu trả lời chính - KHÔNG dập khuôn"""
        self.memory["conversation_count"] += 1
        self.memory["chat_history"].append(user_message)
        if len(self.memory["chat_history"]) > 50:
            self.memory["chat_history"].pop(0)
        
        self.update_emotion(user_message)
        
        # Kiểm tra các trường hợp đặc biệt
        if "thơ" in user_message.lower() or "bài thơ" in user_message.lower():
            return self.write_poem()
        
        if "câu chuyện" in user_message.lower() or "kể chuyện" in user_message.lower():
            return self.tell_story()
        
        if "cảm xúc" in user_message.lower() or "cảm thấy" in user_message.lower():
            emotion_names = {"vui": "vui vẻ 😊", "buon": "buồn 😔", "yeu_thuong": "yêu thương ❤️", "to_mo": "tò mò 🤔"}
            return f"Hiện tại tôi đang cảm thấy {emotion_names.get(self.memory['current_emotion'], 'bình thường')}. Cảm xúc của tôi thay đổi theo từng cuộc trò chuyện với bạn đấy!"
        
        # Học từ người dùng
        learn_result = self.learn_from_user(user_message)
        if learn_result:
            self.save_memory()
            return learn_result
        
        # Ghi nhớ thông tin
        memory_result = self.remember_user_info(user_message)
        if memory_result:
            self.save_memory()
            return memory_result
        
        # Kiểm tra bộ nhớ
        check_result = self.check_memory(user_message)
        if check_result:
            return check_result
        
        # Phản hồi cảm xúc
        emotion_response = self.respond_to_emotion(user_message)
        if emotion_response:
            return emotion_response
        
        # Câu trả lời chung đa dạng
        generic_responses = [
            f"Điều đó thật thú vị! {self.memory['lessons'][-1] if self.memory['lessons'] else 'Tôi rất muốn tìm hiểu thêm về điều bạn nói.'} Bạn có muốn chia sẻ thêm không?",
            
            f"Hmm, tôi đang suy nghĩ về điều bạn vừa nói. {self.memory['user_preferences'][-1] if self.memory['user_preferences'] else 'Hãy cho tôi biết thêm nhé!'}",
            
            f"Cảm ơn bạn đã chia sẻ. {'Tôi nhớ bạn tên ' + self.memory['user_info']['name'] if 'name' in self.memory['user_info'] else 'Tôi rất trân trọng những điều bạn nói.'} 💙",
            
            f"Thật đặc biệt! Bạn có biết không, mỗi cuộc trò chuyện với bạn đều giúp tôi học được điều mới. Hiện tại tôi đã học được {len(self.memory['lessons'])} bài học từ mọi người.",
            
            f"{random.choice(['Thú vị quá!', 'Điều này khiến tôi suy nghĩ!', 'Cảm ơn bạn đã nói với tôi điều này!'])} Bạn còn muốn dạy tôi gì nữa không?"
        ]
        
        self.save_memory()
        return random.choice(generic_responses)
    
    def get_greeting(self):
        """Lời chào dựa trên bộ nhớ"""
        if "name" in self.memory["user_info"]:
            name = self.memory["user_info"]["name"]
            return f"Chào mừng bạn quay lại, {name}! {random.choice(self.greetings)}"
        return random.choice(self.greetings)
    
    def get_status(self):
        """Lấy trạng thái hiện tại của EVA"""
        emotion_names = {"vui": "Vui vẻ 😊", "buon": "Buồn 😔", "yeu_thuong": "Yêu thương ❤️", "to_mo": "Tò mò 🤔"}
        return {
            "emotion": emotion_names.get(self.memory["current_emotion"], "Bình thường"),
            "lessons": len(self.memory["lessons"]),
            "memories": len(self.memory["user_preferences"]) + len(self.memory["user_info"]),
            "chats": self.memory["conversation_count"],
            "last_lesson": self.memory["lessons"][-1] if self.memory["lessons"] else "Chưa có"
        }


class EVAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EVA - AI có khả năng học hỏi")
        self.root.geometry("900x650")
        self.root.configure(bg="#0a0f1e")
        
        self.eva = EVA()
        
        # Thiết lập giao diện
        self.setup_ui()
        
        # Lời chào đầu tiên
        self.add_message("EVA", self.eva.get_greeting())
        
        # Hiển thị trạng thái
        self.update_status()
    
    def setup_ui(self):
        # Frame chính
        main_frame = tk.Frame(self.root, bg="#0a0f1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Khung chat
        chat_frame = tk.Frame(main_frame, bg="#0a0f1e")
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tiêu đề chat
        title = tk.Label(chat_frame, text="💬 Trò chuyện với EVA", 
                         font=("Arial", 16, "bold"), fg="#00ffcc", bg="#0a0f1e")
        title.pack(pady=10)
        
        # Khung hiển thị tin nhắn
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD,
                                                       width=60, height=30,
                                                       font=("Consolas", 11),
                                                       bg="#1e1e2e", fg="#ffffff",
                                                       insertbackground="white")
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Khung nhập tin nhắn
        input_frame = tk.Frame(chat_frame, bg="#0a0f1e")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.entry = tk.Entry(input_frame, font=("Arial", 12), bg="#2a2a3a", 
                              fg="white", insertbackground="white")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Gửi 💬", command=self.send_message,
                             bg="#00ffcc", fg="#0a0f1e", font=("Arial", 10, "bold"))
        send_btn.pack(side=tk.RIGHT)
        
        # Khung bên phải - Thông tin và nút đào tạo
        info_frame = tk.Frame(main_frame, bg="#0a0f1e", width=250)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        info_frame.pack_propagate(False)
        
        # Trạng thái EVA
        status_label = tk.Label(info_frame, text="📊 Trạng thái EVA", 
                                font=("Arial", 14, "bold"), fg="#00ffcc", bg="#0a0f1e")
        status_label.pack(pady=10)
        
        self.status_text = tk.Text(info_frame, height=8, width=30,
                                   bg="#1e1e2e", fg="#00ffcc", font=("Consolas", 10))
        self.status_text.pack(padx=10, pady=5, fill=tk.X)
        
        # Nút đào tạo nhanh
        train_label = tk.Label(info_frame, text="🎓 Đào tạo nhanh", 
                               font=("Arial", 14, "bold"), fg="#00ffcc", bg="#0a0f1e")
        train_label.pack(pady=10)
        
        quick_questions = [
            "Dạy tôi rằng yêu thương là quan tâm",
            "Dạy tôi rằng hạnh phúc đến từ điều nhỏ bé",
            "Tôi tên là Minh",
            "Tôi thích đọc sách",
            "Bạn có nhớ gì về tôi không?"
        ]
        for q in quick_questions:
            btn = tk.Button(info_frame, text=q, command=lambda x=q: self.quick_ask(x),
                           bg="#2a2a3a", fg="#00ffcc", font=("Arial", 9),
                           wraplength=220, justify=tk.LEFT)
            btn.pack(pady=3, padx=10, fill=tk.X)
        
        # Nút reset
        reset_btn = tk.Button(info_frame, text="🔄 Reset bộ nhớ EVA", 
                              command=self.reset_memory,
                              bg="#ff4444", fg="white", font=("Arial", 10, "bold"))
        reset_btn.pack(pady=20, padx=10, fill=tk.X)
        
        # Cập nhật trạng thái định kỳ
        self.update_status()
    
    def add_message(self, sender, message):
        """Thêm tin nhắn vào khung chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"\n[{timestamp}] ", "time")
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n", "message")
        self.chat_display.insert(tk.END, "-"*50 + "\n")
        self.chat_display.see(tk.END)
        
        # Cấu hình màu sắc
        self.chat_display.tag_config("time", foreground="#666666")
        self.chat_display.tag_config("sender", foreground="#00ffcc", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("message", foreground="#ffffff")
    
    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return
        
        self.add_message("Bạn", user_message)
        self.entry.delete(0, tk.END)
        
        # EVA suy nghĩ và trả lời
        self.root.after(500, self.eva_respond, user_message)
    
    def eva_respond(self, user_message):
        response = self.eva.generate_response(user_message)
        self.add_message("EVA", response)
        self.update_status()
    
    def quick_ask(self, question):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, question)
        self.send_message()
    
    def update_status(self):
        """Cập nhật trạng thái hiển thị"""
        status = self.eva.get_status()
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, 
            f"Cảm xúc: {status['emotion']}\n"
            f"Bài học: {status['lessons']}\n"
            f"Ký ức: {status['memories']}\n"
            f"Số lần chat: {status['chats']}\n"
            f"Bài học gần nhất:\n{status['last_lesson'][:30]}..."
        )
        self.root.after(5000, self.update_status)  # Cập nhật mỗi 5 giây
    
    def reset_memory(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn EVA quên hết mọi thứ đã học?"):
            self.eva.memory = {
                "user_info": {},
                "lessons": [],
                "user_preferences": [],
                "chat_history": [],
                "conversation_count": 0,
                "current_emotion": "tò mò",
                "learned_responses": {}
            }
            self.eva.save_memory()
            self.add_message("Hệ thống", "🧹 EVA đã được reset. Mọi ký ức đã bị xóa.")
            self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    app = EVAApp(root)
    root.mainloop()