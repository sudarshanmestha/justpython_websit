nextjs-portfolio/
├── app/auth/forgot-password/
│   ├── page.tsx                    ← REPLACE your existing file
│   └── [uid]/[token]/
│       └── page.tsx                ← CREATE this (new file)
└── lib/
    └── api.ts                      ← REPLACE your existing file
    
also : doc.http   
    
Django: settings.py, urls.py, 
        your auth app's models.py, serializers.py, views.py, and urls.py
        
Next.js: your folder structure, existing auth pages (login/register), and any API utility files ( api.ts , AuthContext.tsx )        


remaining step:
reset-password/[uid]/[token]/page.tsx