(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[405],{8312:function(e,t,s){(window.__NEXT_P=window.__NEXT_P||[]).push(["/",function(){return s(2609)}])},442:function(e,t,s){"use strict";s.d(t,{C:function(){return l}});var n=s(7294),r=s(7655);let l=()=>(0,n.useContext)(r.f)},7655:function(e,t,s){"use strict";s.d(t,{f:function(){return l},h:function(){return a}});var n=s(5893),r=s(7294);let l=r.createContext({queryData:{},setQueryData:()=>{}}),a=e=>{let[t,s]=(0,r.useState)([]);return(0,n.jsx)(l.Provider,{value:{queryData:t,setQueryData:s},children:e.children})}},2609:function(e,t,s){"use strict";s.r(t),s.d(t,{default:function(){return h}});var n=s(5893),r=s(442),l=s(6154),a=s(7294),i=()=>{(0,a.useEffect)(()=>{document.body.style.overflow="hidden"},[]);let{queryData:e,setQueryData:t}=(0,r.C)(),[s,i]=(0,a.useState)(""),[o,c]=(0,a.useState)("Absolute"),[d,u]=(0,a.useState)(!1),[h,x]=(0,a.useState)(!1),w=()=>{u(!d)},v=async()=>{x(!0);let e=new URLSearchParams([["strategy",'"'+o+'"'],["query",'"'+s+'"']]);try{let s=await l.Z.get("/api/nlpSearch?".concat(e)),{result:n,data:r}=s.data;"success"===n.trim()&&t(r),x(!1)}catch(e){console.error("Error:",e),x(!1)}};return(0,n.jsxs)("div",{children:[(0,n.jsxs)("div",{className:"z-10 absolute top-5 left-7 flex flex-row gap-5",children:[(0,n.jsxs)("div",{className:"shadow-md rounded-xl flex flex-row",children:[(0,n.jsx)("input",{type:"text",placeholder:'Try "Fires in ON in 05/2021" (nltk)',className:"p-3 rounded-s-xl text-black w-80",value:s,onChange:e=>{i(e.target.value)},onKeyDown:e=>{"Enter"===e.key&&v()}}),(0,n.jsx)("button",{className:"p-3 text-white bg-gray-500 bg-opacity-75 rounded-e-xl",onClick:v,disabled:h,children:h?(0,n.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:1.5,stroke:"currentColor",className:"w-6 h-6",children:(0,n.jsx)("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"})}):(0,n.jsx)("div",{children:"Search"})})]}),(0,n.jsx)("div",{className:"flex flex-row",children:(0,n.jsxs)("div",{className:"rounded-xl shadow-md",children:[(0,n.jsx)("button",{className:"p-3 text-white rounded-s-xl ".concat("Absolute"===o?"bg-gray-600":"bg-gray-500 bg-opacity-75"),onClick:()=>c("Absolute"),children:"Absolute"}),(0,n.jsx)("button",{className:"p-3 text-white rounded-e-xl ".concat("Optimistic"===o?"bg-gray-600":"bg-gray-500 bg-opacity-75"),onClick:()=>c("Optimistic"),children:"Optimistic"})]})})]}),(0,n.jsx)("div",{className:"z-10 absolute top-5 right-7 flex flex-row rounded-xl shadow-md ",children:(0,n.jsxs)("button",{className:"flex flex-row gap-1 bg-gray-500 p-3 rounded-xl bg-opacity-75 items-center",onClick:w,children:[(0,n.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:1.5,stroke:"currentColor",className:"w-5 h-5 text-white",children:(0,n.jsx)("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M19.5 12h-15m0 0l6.75 6.75M4.5 12l6.75-6.75"})}),(0,n.jsx)("div",{className:"text-white",children:"Data"})]})}),(0,n.jsx)("div",{className:"text-black overflow-hidden z-20 absolute top-0 -right-0 h-screen bg-white p-7 transition-transform duration-500 ease-in-out ".concat(d?"translate-x-0":"translate-x-full"),children:(0,n.jsxs)("div",{className:"flex flex-col gap-5",children:[(0,n.jsx)("button",{onClick:w,children:(0,n.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",fill:"none",viewBox:"0 0 24 24",strokeWidth:1.5,stroke:"currentColor",className:"w-6 h-6",children:(0,n.jsx)("path",{strokeLinecap:"round",strokeLinejoin:"round",d:"M6 18L18 6M6 6l12 12"})})}),e&&e.length>0?(0,n.jsx)("div",{className:"overflow-auto",children:e.map((e,t)=>(0,n.jsxs)("div",{children:[(0,n.jsx)("div",{children:e.DATE}),(0,n.jsx)("div",{children:e.PROVINCE_CODE}),(0,n.jsx)("div",{children:e.LATITUDE}),(0,n.jsx)("div",{children:e.LONGITUDE}),(0,n.jsx)("div",{children:e.CAUSE}),(0,n.jsx)("div",{children:e.SIZE_HA})]},t))}):(0,n.jsx)("div",{children:"No data now..."})]})})]})},o=s(7655),c=s(5152),d=s.n(c);let u=d()(()=>Promise.all([s.e(668),s.e(483)]).then(s.bind(s,8483)),{loadableGenerated:{webpack:()=>[8483]},ssr:!1});var h=e=>{let{}=e;return(0,n.jsxs)(o.h,{children:[(0,n.jsx)(i,{}),(0,n.jsx)(u,{})]})}}},function(e){e.O(0,[530,774,888,179],function(){return e(e.s=8312)}),_N_E=e.O()}]);