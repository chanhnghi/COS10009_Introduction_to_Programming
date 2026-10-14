import os 
import json 

class Leaderboard:
    def __init__(self, filename = "score.json"):
        self.filename = filename 
        self.scores = self.load_scores()
        self.current_tab = "Easy"

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data =  json.load(f)
            if not isinstance(data, dict):
                data = {"Easy":[], "Medium":[], "Hard":[]}
            for level in ["Easy", "Medium","Hard"]:
                if level not in data:
                    data[level] = []
            return data
        return {"Easy": [], "Medium": [], "Hard": []}
    
    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f, indent=3)
    
    def add_scores(self, name, time):
        self.scores[self.current_tab].append({"name" : name , 
                            "time" : time })
        self.sort_scores()
        self.save_scores()

    def sort_scores(self):
        active_list = self.scores[self.current_tab]
        n = len(active_list)
        for i in range(n):
            min_index = i 
            for j in range(i+1, n):
                if active_list[j]["time"] < active_list[min_index]['time']:
                    min_index = j 
            active_list[i], active_list[min_index] = active_list[min_index], active_list[i]
        self.scores[self.current_tab] = active_list[:12]

    def sort_by_name(self):
        active_list = self.scores[self.current_tab]
        n = len (active_list)
        for i in range(n):
            min_index = i 
            for j in range(i+1, n):
                if active_list[j]['name'].lower() < active_list[min_index]['name'].lower() :
                    min_index = j 
            active_list[i] , active_list[min_index] = active_list[min_index], active_list[i]

    def search_player(self, target_name):
        active_list = self.scores[self.current_tab]
        self.sort_by_name() 
        low = 0 
        high = len(active_list) -1 
        found_record = None

        while low <= high :
            mid = (high + low) // 2
            if  active_list[mid]['name'].lower() == target_name.lower() :
                found_record = active_list[mid]
                break
            if target_name.lower() < active_list[mid]['name'].lower() :
                high = mid - 1
            else:
                low = mid + 1

        self.sort_scores()

        if found_record:
            for i, record in enumerate(active_list):
                if record['name'] == found_record['name'] and record['time'] == found_record['time']:
                    return i 
        return -1
    
if __name__ == "__main__":
    lb = Leaderboard()
    
    # Test tìm một tên có trong score.json (ví dụ "Kaka")
    result = lb.search_player("tesing5")
    if result:
        print(f"Tìm thấy: {result['name']} với thời gian {result['time']}s")
    else:
        print("Không tìm thấy người chơi này.")
            
            
