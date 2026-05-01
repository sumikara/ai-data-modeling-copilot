from __future__ import annotations
import os, json
from pathlib import Path
from typing import Dict,Any
try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

CFG=Path('config/models.yaml')

def _cfg()->Dict[str,Any]:
    if not CFG.exists():
        return {}
    if yaml is None:
        return {}
    return yaml.safe_load(CFG.read_text())

def route(prompt:str, provider:str)->Dict[str,Any]:
    c=_cfg(); provider=provider.lower()
    if provider=='mock':
        return {"ok":True,"text":"{}","provider":"mock"}
    if provider=='openai':
        if not os.getenv('OPENAI_API_KEY'): return {"ok":False,"error":"missing OPENAI_API_KEY","provider":"openai"}
        from openai import OpenAI
        model=c.get('openai',{}).get('model','gpt-4o-mini')
        cli=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        r=cli.chat.completions.create(model=model,messages=[{"role":"user","content":prompt}],temperature=c.get('openai',{}).get('temperature',0))
        return {"ok":True,"text":r.choices[0].message.content or "","provider":"openai"}
    if provider=='gemini':
        if not os.getenv('GEMINI_API_KEY'): return {"ok":False,"error":"missing GEMINI_API_KEY","provider":"gemini"}
        from google import genai
        client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        model=c.get('gemini',{}).get('model','gemini-2.5-flash')
        r=client.models.generate_content(model=model,contents=[prompt])
        return {"ok":True,"text":r.text or "","provider":"gemini"}
    if provider=='anthropic':
        if not os.getenv('ANTHROPIC_API_KEY'): return {"ok":False,"error":"missing ANTHROPIC_API_KEY","provider":"anthropic"}
        try:
            import anthropic
            model=c.get('anthropic',{}).get('model','claude-sonnet-4-6')
            cli=anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            r=cli.messages.create(model=model,max_tokens=3000,messages=[{"role":"user","content":prompt}])
            text="".join([b.text for b in r.content if getattr(b,'type','')=='text'])
            return {"ok":True,"text":text,"provider":"anthropic"}
        except Exception as e:
            return {"ok":False,"error":f"anthropic unavailable: {e}","provider":"anthropic"}
    return {"ok":False,"error":f"unsupported provider {provider}","provider":provider}
