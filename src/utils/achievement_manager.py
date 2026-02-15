import json, os, time

class AchievementManager:
    def __init__(self, path='data/achievements.json'):
        self.path = path

    def get_all(self):
        if not os.path.exists(self.path): return []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list): return []
                return [a for a in data if isinstance(a, dict) and 'id' in a]
        except: return []

    def record(self, aid, title, desc):
        data = self.get_all()
        if not any(a.get('id') == aid for a in data):
            data.append({
                'id': aid, 
                'title': title, 
                'description': desc, 
                'timestamp': time.ctime()
            })
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        return False

    def get_message_blocks(self, limit=1900):
        achievements = self.get_all()
        blocks = []
        current_block = "# 🏆 WiseClaw OS: Achievements Gallery\n\n"

        for a in achievements:
            line = f"**{a.get('title', 'Unknown')}** ({a.get('timestamp', 'N/A')})\n> {a.get('description', 'No description.')}\n\n"
            if len(current_block) + len(line) > limit:
                blocks.append(current_block)
                current_block = line
            else:
                current_block += line

        blocks.append(current_block)
        return blocks