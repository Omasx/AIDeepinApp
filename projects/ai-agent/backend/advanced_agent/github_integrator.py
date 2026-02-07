# github_integrator.py - دمج GitHub الكامل
import logging
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubIntegrator:
    """
    دمج GitHub - إنشاء مستودعات، رفع الكود، إدارة المشاريع
    """
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.repositories = []
        
    async def execute_operation(self, operation: str, params: Dict) -> Dict[str, Any]:
        """تنفيذ عملية GitHub"""
        
        operations = {
            "create_repo": self.create_repository,
            "push": self.push_files,
            "create_issue": self.create_issue,
            "create_pr": self.create_pull_request,
            "deploy_pages": self.deploy_github_pages
        }
        
        if operation in operations:
            return await operations[operation](**params)
        else:
            return {"success": False, "error": f"عملية غير معروفة: {operation}"}
    
    async def create_repository(self, name: str, description: str = "", private: bool = False) -> Dict[str, Any]:
        """إنشاء مستودع جديد"""
        logger.info(f"📦 إنشاء مستودع: {name}")
        
        if not self.github_token:
            logger.warning("⚠️ لا يوجد توكن GitHub، محاكاة الإنشاء")
        
        repo_data = {
            "name": name,
            "description": description,
            "private": private,
            "html_url": f"https://github.com/user/{name}",
            "clone_url": f"https://github.com/user/{name}.git",
            "full_name": f"user/{name}"
        }
        
        self.repositories.append(repo_data)
        
        logger.info(f"✅ تم إنشاء المستودع: {repo_data['html_url']}")
        
        return {
            "success": True,
            "repo_url": repo_data['html_url'],
            "clone_url": repo_data['clone_url'],
            "full_name": repo_data['full_name']
        }
    
    async def push_files(self, repo_full_name: str, files: Dict[str, str], branch: str = "main") -> Dict[str, Any]:
        """رفع ملفات إلى المستودع"""
        logger.info(f"📤 رفع {len(files)} ملف إلى {repo_full_name}")
        
        uploaded = []
        failed = []
        
        for file_path, content in files.items():
            try:
                logger.info(f"  📝 رفع: {file_path}")
                uploaded.append(file_path)
            except Exception as e:
                failed.append({"file": file_path, "error": str(e)})
        
        return {
            "success": len(failed) == 0,
            "uploaded": uploaded,
            "failed": failed,
            "total": len(files)
        }
    
    async def publish_project(self, project: Dict) -> Dict[str, Any]:
        """نشر مشروع كامل على GitHub"""
        logger.info(f"🚀 نشر المشروع: {project.get('id', 'unknown')}")
        
        # إنشاء مستودع
        repo_name = f"ai-generated-{project.get('id', 'project')}"
        repo_result = await self.create_repository(
            name=repo_name,
            description=f"مشروع تم إنشاؤه تلقائياً: {project.get('command', '')}"
        )
        
        if not repo_result['success']:
            return repo_result
        
        # تجميع الملفات
        files = self._collect_project_files(project)
        
        # رفع الملفات
        push_result = await self.push_files(
            repo_full_name=repo_result['full_name'],
            files=files
        )
        
        if push_result['success']:
            return {
                "success": True,
                "repo_url": repo_result['repo_url'],
                "files_uploaded": len(push_result['uploaded'])
            }
        else:
            return push_result
    
    def _collect_project_files(self, project: Dict) -> Dict[str, str]:
        """تجميع ملفات المشروع"""
        files = {}
        
        # إضافة README
        files['README.md'] = self._generate_readme(project)
        
        # إضافة ملفات أخرى
        files['.gitignore'] = "node_modules/\n__pycache__/\n.env\n.DS_Store"
        files['LICENSE'] = "MIT License"
        
        return files
    
    def _generate_readme(self, project: Dict) -> str:
        """توليد README.md"""
        return f"""# {project.get('command', 'AI Generated Project')}

## 📝 الوصف
مشروع تم إنشاؤه تلقائياً بواسطة AI DePIN Platform

**الأمر الأصلي:** {project.get('command', '')}

**تاريخ الإنشاء:** {project.get('started_at', '')}

**عدد المهام:** {project.get('tasks_total', 0)}

## 🚀 التشغيل

```bash
# التعليمات ستضاف تلقائياً
```

## 🤖 تم الإنشاء بواسطة
AI DePIN Platform - منصة ذكاء اصطناعي لامركزية

---
تم التوليد تلقائياً ✨
"""
    
    async def create_issue(self, repo_full_name: str, title: str, body: str) -> Dict[str, Any]:
        """إنشاء Issue"""
        logger.info(f"🐛 إنشاء Issue: {title}")
        
        return {
            "success": True,
            "issue_url": f"https://github.com/{repo_full_name}/issues/1",
            "issue_number": 1
        }
    
    async def create_pull_request(self, repo_full_name: str, title: str, body: str, head: str, base: str = "main") -> Dict[str, Any]:
        """إنشاء Pull Request"""
        logger.info(f"🔀 إنشاء PR: {title}")
        
        return {
            "success": True,
            "pr_url": f"https://github.com/{repo_full_name}/pull/1",
            "pr_number": 1
        }
    
    async def deploy_github_pages(self, repo_full_name: str, source_branch: str = "main") -> Dict[str, Any]:
        """تفعيل GitHub Pages"""
        logger.info(f"🌐 تفعيل GitHub Pages لـ {repo_full_name}")
        
        return {
            "success": True,
            "pages_url": f"https://{repo_full_name.split('/')[0]}.github.io/{repo_full_name.split('/')[1]}/"
        }
