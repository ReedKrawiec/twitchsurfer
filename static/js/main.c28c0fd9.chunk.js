(this.webpackJsonpui=this.webpackJsonpui||[]).push([[0],{39:function(e,t,a){e.exports=a(86)},44:function(e,t,a){},46:function(e,t,a){e.exports=a.p+"static/media/logo.ee7cd8ed.svg"},50:function(e,t,a){},51:function(e,t,a){},86:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),i=a(35),c=a.n(i),s=(a(44),a(8)),l=a.n(s),o=a(20),m=a(13),u=a(14),d=a(16),h=a(15),f=a(9),p=a(36),v=(a(46),a(21)),E=a(37),_=a.n(E),g=a(3),b=a.n(g),w=(r.a.Component,a(49),a(50),a(51),a(1)),y=a.n(w),N=(a(52),a(38)),k=a.n(N),j=window.innerWidth/24;j<70&&(j=70);var x=r.a.createContext({}),O=r.a.createContext({}),C=r.a.createContext({});var S=function(e){var t=Object(n.useContext)(O),a=function(){t.setTime(e.time.subtract(2,"hours"))},i={width:j};return 2===e.index&&(i.backgroundColor="purple"),0===e.time.hours()&&0===e.time.minutes()?r.a.createElement("div",{className:"timeline-header-label timeline-header-label-day",style:i,onClick:function(){a()}},r.a.createElement("p",{className:"timeline-header-day"},e.time.format("M/D")),r.a.createElement("p",null,e.time.format("h:mm a"))):r.a.createElement("div",{className:"timeline-header-label",style:i,onClick:function(){a()}},r.a.createElement("p",null,e.time.format("h:mm")),r.a.createElement("p",null,e.time.format("a")))};function W(e){var t=y()(e.start);t.subtract(1,"hour");for(var a=[],n=0,i=0;n<window.innerWidth;n+=j,i++)a.push(r.a.createElement(S,{time:y()(t.add(1,"hour")),index:i,key:i}));return r.a.createElement("div",{className:"timeline-header-holder"},a)}function T(e){var t,a=Object(n.useContext)(C),i=y()(e.start),c=[],s=0,l=Object(p.a)(e.streams);try{var o=function(){var n=t.value,l=y.a.duration(n.start_time.diff(i)).asMinutes()/60*j,o=y.a.duration(n.end_time.diff(n.start_time)).asMinutes()/60*j;c.push(r.a.createElement("div",{key:s,className:"time-stream-container",style:{left:l}},r.a.createElement("img",{className:"time-stream-picture",src:n.profile_picture}),r.a.createElement("svg",{style:{fill:e.color},className:"timeline-stream",height:"50",width:o+25,onClick:function(){a.setUser({name:n.name,description:n.description})}},r.a.createElement("g",null,r.a.createElement("circle",{cx:"15",cy:"25",r:"15"}),r.a.createElement("rect",{x:"15",y:"17.5",width:o,height:"15"}),r.a.createElement("text",{x:"50%",y:"20%","dominant-baseline":"middle","text-anchor":"middle"},n.name),r.a.createElement("circle",{cx:o+10,cy:"25",r:"15"}))))),s++};for(l.s();!(t=l.n()).done;)o()}catch(m){l.e(m)}finally{l.f()}return r.a.createElement("div",{className:"timeline-render-line"},c)}function A(e){for(var t=[],a=0;a<e.grouped_streams.length;a++)t.push(r.a.createElement(T,{start:e.start,key:a,color:e.color,streams:e.grouped_streams[a]}));return r.a.createElement("div",null,t)}function B(e){if(e.streams.length>0){var t=function(e){for(var t=[];e.length>0;){var a=e[0];e.splice(0,1);for(var n=!1,r=0;r<t.length&&!n;r++)for(var i=0;i<t[r].length;i++){var c=t[r][i];if(i===t[r].length-1){if(a.start_time.isAfter(y()(c.end_time).add(1,"hour"))){n=!0,t[r].push(a);break}}else if(a.start_time.isAfter(y()(c.end_time).add(1,"hour")&&a.end_time.isBefore(y()(t[r][i+1].start_time)))){n=!0,t[r].push(a);break}}n||(t.push([]),t[t.length-1].push(a))}return t}(e.streams);return r.a.createElement("div",{className:"category-container"},r.a.createElement("div",{style:{color:e.color},className:"timeline-category"},r.a.createElement("div",{className:"timeline-category-container"},r.a.createElement("p",{className:"timeline-category-name"},e.name),r.a.createElement("div",{style:{backgroundColor:e.color},className:"timeline-category-bar"}))),r.a.createElement("div",{className:"category-holder"}),r.a.createElement(A,{grouped_streams:t,start:e.start,color:e.color}))}return r.a.createElement("div",null)}function I(e){var t=Object(n.useContext)(C),a=r.a.createElement("a",{className:"site_login",href:e.auth_string},"Login With Twitch");return e.username&&(a=r.a.createElement("p",{className:"site_login"},e.username," ",r.a.createElement("a",{className:"site_logout",href:"./"},"LOGOUT"))),r.a.createElement("div",{className:"header-bar"},r.a.createElement("div",{className:"header-container"},r.a.createElement("div",{className:"info-box"},r.a.createElement("p",{className:"site_logo"},"TWITCH SURFER"),a,r.a.createElement("div",{className:"streamer-info"},r.a.createElement("p",{className:"streamer-name"},t.user.name),r.a.createElement("div",{className:"streamer-desc"},r.a.createElement("p",null,t.user.description)))),r.a.createElement(k.a,{targetClass:"streamer-embed",channel:t.user.name,width:"500px",height:"100%",layout:"video"})))}var L=function(e){var t=Object(n.useState)(y()().subtract(1,"hour").subtract(y()().minutes(),"minutes")),a=Object(f.a)(t,2),i=a[0],c=a[1],s=Object(n.useContext)(x),l=i,o=[];if(s.valid){var m=y()(l).startOf("week"),u=(y()(l).diff(m,"minutes"),y()(l).add(window.innerWidth/j*60,"minutes")),d=!1;s.data.forEach((function(e){var t="https://static-cdn.jtvnw.net/jtv_user_pictures/xqcow-profile_image-9298dca608632101-300x300.jpeg",a="No description given.";e.description&&(a=e.description),e.profile&&(t=e.profile);for(var n=void 0,r=0;r<e.schedule.length;r++)d?(o.push({name:e.streamer,profile_picture:t,description:a,start_time:n,end_time:y()(m).add(30*e.schedule[r],"minutes")}),y()(n).day()<4&&o.push({name:e.streamer,profile_picture:t,description:a,start_time:y()(n).add(1,"week"),end_time:y()(m).add(30*e.schedule[r],"minutes").add(1,"week")}),d=!1):(n=y()(m).add(30*e.schedule[r],"minutes"),d=!0);d&&(o.push({name:e.streamer,profile_picture:t,description:a,start_time:y()(m).add(30*e.schedule[e.schedule.length-1],"minutes"),end_time:y()(m).add(10080,"minutes")}),y()(n).day()<4&&o.push({name:e.streamer,profile_picture:t,description:a,start_time:y()(m).add(30*e.schedule[e.schedule.length-1],"minutes").add(1,"week"),end_time:y()(m).add(10080,"minutes").add(1,"week")})),d=!1})),o=o.filter((function(e){return e.start_time.isAfter(l)&&e.start_time.isBefore(u)||e.end_time.isAfter(l)&&e.end_time.isBefore(u)}))}return r.a.createElement(O.Provider,{value:{time:i,setTime:c}},r.a.createElement("div",{className:"timeline"},r.a.createElement("div",{className:"timeline-time-labels"},r.a.createElement(W,{start:l})),r.a.createElement("div",{className:"timeline-body"},r.a.createElement(B,{start:l,streams:o,name:"FOLLOWING",color:"#88fffb"}))))};function U(e,t,a){var n={Authorization:"Bearer ".concat(t)};return a&&(n["Client-ID"]=a),fetch(e,{headers:n})}var M=function(e){Object(d.a)(a,e);var t=Object(h.a)(a);function a(){return Object(m.a)(this,a),t.apply(this,arguments)}return Object(u.a)(a,[{key:"render",value:function(){return this.props.condition?this.props.children:r.a.createElement("div",null)}}]),a}(r.a.Component);function R(){return r.a.createElement("div",{className:"loader"},r.a.createElement("p",null,"TWITCH SURFER"),r.a.createElement("p",null,"LOADING"))}var z=function(){var e=Object(n.useState)({name:"",description:"Select a stream!"}),t=Object(f.a)(e,2),a=t[0],i=t[1],c=Object(n.useState)({valid:!1,data:void 0}),s=Object(f.a)(c,2),m=s[0],u=s[1],d=Object(n.useState)(void 0),h=Object(f.a)(d,2),p=h[0],v=h[1],E="https://twitchsurfer.herokuapp.com",_=JSON.stringify({userinfo:{email:null,email_verified:null,picture:null,preferred_username:null}}),g="https://id.twitch.tv/oauth2/authorize?client_id=".concat("sh58je5z5mtatvjc7jfc1m6bgfvt94","&redirect_uri=").concat("https://reedkrawiec.github.io/twitchsurfer","&response_type=").concat("token+id_token","&scope=").concat("openid+user:edit:follows+user:read:email","&claims=").concat(_);return Object(n.useEffect)((function(){if(window.location.hash&&!m.valid){var e=window.location.hash.slice(1).split("&").map((function(e){return e.split("=")})),t={access_token:e[0][1],id_token:e[1][1],scope:e[2][1],token_type:e[3][1]};(function(){var e=Object(o.a)(l.a.mark((function e(){var a,n;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,U("https://id.twitch.tv/oauth2/userinfo",t.access_token);case 2:return a=e.sent,e.next=5,a.json();case 5:return a=e.sent,v(a.preferred_username),e.next=9,fetch("".concat(E,"/get_schedule?access=").concat(t.access_token,"&id=").concat(a.sub));case 9:return n=e.sent,e.next=12,n.json();case 12:n=e.sent,n.length,console.log(n),u({valid:!0,data:n});case 16:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}})()()}else{(function(){var e=Object(o.a)(l.a.mark((function e(){var t;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("".concat(E,"/get_default"));case 2:return t=e.sent,e.next=5,t.json();case 5:t=e.sent,u({valid:!0,data:t});case 7:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}})()()}}),[]),r.a.createElement("div",{className:"loader_holder"},r.a.createElement(M,{condition:m.valid},r.a.createElement(x.Provider,{value:m},r.a.createElement(C.Provider,{value:{user:a,setUser:i}},r.a.createElement("div",{className:"App"},r.a.createElement(I,{auth_string:g,username:p}),r.a.createElement(L,null))))),r.a.createElement(M,{condition:!m.valid},r.a.createElement(R,null)))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));c.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(z,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[39,1,2]]]);
//# sourceMappingURL=main.c28c0fd9.chunk.js.map