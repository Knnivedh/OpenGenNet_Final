## 🧪 **TEST COMMANDS AFTER .ENV UPLOAD**

### **Quick Test:**
```bash
curl https://opengennet-ai.vercel.app/health
```

### **Expected Result (After Environment Variables Load):**
```json
{
  "version": "1.1.4",
  "groq_key_present": true,
  "providers": 4,
  "env_debug": {
    "GROQ_FAST_KEY": "present",
    "GROQ_CODING_KEY": "present", 
    "DEEPSEEK_KEY": "present",
    "QWEN_KEY": "present"
  }
}
```

### **AI Chat Test:**
```bash
curl -X POST https://opengennet-ai.vercel.app/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Test AI response with expert knowledge.", "use_expert_context": true}'
```

### **Expected AI Response:**
```json
{
  "response": "Hello! I'm an enhanced AI system with expert knowledge...",
  "provider": "groq",
  "expert_context_used": true
}
```

---

## 🎯 **AFTER UPLOADING .ENV:**

1. **Upload** the `.env` file using "Import .env" button
2. **Verify** 4 variables appear in the dashboard  
3. **Redeploy** from Deployments tab
4. **Test** the health endpoint
5. **Enjoy** your fully activated AI system! 🚀

**Your enhanced OpenGenNet AI with 4 providers + expert knowledge will be ready!**
