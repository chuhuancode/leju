webpackJsonp([4],{Mfhj:function(s,t){},faps:function(s,t){},kafJ:function(s,t,e){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i=e("mtWM"),n=e.n(i),a=e("GQaK"),o={name:"questionslist",props:["questions"],mounted:function(){this.createScroller()},methods:{createScroller:function(){this.scroller=new a.a(this.$refs.wrapper)}},watch:{questions:function(){var s=this;this.$nextTick(function(){s.scroller.refresh()})}}},r={render:function(){var s=this,t=s.$createElement,e=s._self._c||t;return e("div",{ref:"wrapper",staticClass:"wrapper"},[e("ul",{staticClass:"questions-container"},s._l(s.questions,function(t,i){return e("li",{staticClass:"questions-list border-bottom",class:[0===i?"":"padding-top"]},[e("div",[e("div",{staticClass:"questions-img-container"},[e("img",{directives:[{name:"lazy",rawName:"v-lazy",value:t.imgUrl,expression:"item.imgUrl"}],staticClass:"questions-img"}),s._v(" "),e("span",{staticClass:"username"},[s._v(s._s(t.username))])]),s._v(" "),e("div",{staticClass:"questions-desc"},[e("span",{staticClass:"ask"},[s._v("问")]),s._v("\n          "+s._s(t.question)+"\n        ")]),s._v(" "),e("p",{staticClass:"common time"},[s._v("提问于 "+s._s(t.time))]),s._v(" "),e("div",[e("span",{staticClass:"common reply-count"},[s._v(s._s(t.replyCount)+"人回答")]),s._v(" "),e("span",{staticClass:"common"},[s._v(s._s(t.browseCount)+"人浏览")])])]),s._v(" "),e("span",{staticClass:"questions-style border"},[s._v(s._s(t.style))])])}))])},staticRenderFns:[]},c={name:"queations",data:function(){return{questionsInfo:[],isLogin:!1,userInfo:""}},components:{List:e("VU/8")(o,r,!1,function(s){e("faps")},"data-v-0358d727",null).exports},created:function(){try{this.userInfo=JSON.parse(window.localStorage.userInfo)}catch(s){}this.userInfo.state&&(this.isLogin=!0,this.getQuestionsData())},methods:{getQuestionsData:function(){n.a.get("/problem/").then(this.handleGetQuestionsSucc.bind(this)).catch(this.handleGetQuestionsErr.bind(this))},handleGetQuestionsSucc:function(s){this.questionsInfo=s.data.data.question},handleGetQuestionsErr:function(){console.log("获取questions失败")}}},u={render:function(){var s=this.$createElement,t=this._self._c||s;return t("div",{staticClass:"questions"},[t("div",{staticClass:"title border-bottom"},[t("router-link",{staticClass:"iconfont icon",attrs:{to:"/index",tag:"span"}},[this._v("")]),this._v("提问题\n  ")],1),this._v(" "),this.isLogin?t("List",{attrs:{questions:this.questionsInfo}}):this._e(),this._v(" "),this.isLogin?this._e():t("div",{staticClass:"login-first"},[this._v("请先登录")])],1)},staticRenderFns:[]},l=e("VU/8")(c,u,!1,function(s){e("Mfhj")},"data-v-c23a2dfa",null);t.default=l.exports}});
//# sourceMappingURL=4.25dcfd73fa7813bfb339.js.map