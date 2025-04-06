from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.post("/github/commits")
async def get_github_commits(owner: str, repo: str):
    
    # GitHub API 엔드포인트
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    # GitHub API 호출
    response = requests.get(url)
    commits = response.json()
    
    # 커밋 정보 추출
    commit_data = []
    for commit in commits:
        commit_info = {
            "sha": commit["sha"],
            "message": commit["commit"]["message"],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"]
        }
        
        # 수정된 파일 정보 가져오기
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit['sha']}"
        commit_response = requests.get(commit_url)
        commit_detail = commit_response.json()
        
        files_changed = []
        for file in commit_detail["files"]:
            file_info = {
                "filename": file["filename"],
                "status": file["status"],
                "additions": file["additions"],
                "deletions": file["deletions"],
                "changes": file["changes"]
            }
            files_changed.append(file_info)
            
        commit_info["files"] = files_changed
        commit_data.append(commit_info)
    
    return {"commits": commit_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
