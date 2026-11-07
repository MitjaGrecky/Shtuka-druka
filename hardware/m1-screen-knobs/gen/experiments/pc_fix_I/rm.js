// rm.js in out uuid... : drop top-level (segment|via|arc ...) blocks whose uuid/tstamp is listed
const fs=require('fs');const [,,inp,out,listf]=process.argv;const ids=new Set(fs.readFileSync(listf,'utf8').split(/\s+/).filter(Boolean));
const s=fs.readFileSync(inp,'utf8');let o='',i=0,n=0;
while(i<s.length){const m=/\n[ \t]*\((segment|via|arc)\b/g;m.lastIndex=i;const r=m.exec(s);if(!r){o+=s.slice(i);break}
 const st=r.index+1;o+=s.slice(i,st);let d=0,j=s.indexOf('(',st);for(;j<s.length;j++){if(s[j]=='(')d++;else if(s[j]==')'){d--;if(d==0)break}}
 const blk=s.slice(st,j+1);const u=(blk.match(/\((?:uuid|tstamp) "?([0-9a-f-]+)"?\)/)||[])[1];
 if(u&&ids.has(u)){n++;i=j+1;if(s[i]=='\n'){} }else{o+=blk;i=j+1}}
fs.writeFileSync(out,o);console.log('removed',n,'of',ids.size);
