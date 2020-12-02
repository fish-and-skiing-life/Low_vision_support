<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">{{site}}</h1>

        <p class="speak mt-10">読みたいカテゴリーを選んでください。</p>
        <p class="speak ">カテゴリーは{{ categorys }}があります。</p>
        <v-btn class='regnitional-btn' color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
      </v-col>
      
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios';
  export default {
    data(){
      return {
        speech: window.speechSynthesis,
        recognition : "",
        recognitionText: "カテゴリーを選ぶ",
        text: "",
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        site: localStorage.getItem("site"),
        category_dict: {},
        manuscript: [],
        categorys: ""
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/category", {params: { "media": this.site_dict[this.site] }})
        .then(response => {
          this.manuscript.push(this.site + 'で読めるカテゴリーは、')
          this.category_dict = response.data
          for(let key in response.data){
            this.category_dict[key.replace(/\r?\n/g,"")] = response.data[key]
            this.categorys += key.replace(/\r?\n/g,"") + "、"
            if(key.match(/IT/)){
              key = key.replace('IT','アイティー')
            }
            this.manuscript.push(key.replace(/\r?\n/g,""))
          }
          this.manuscript.push("があります。")
        }).catch(() => {
      })
      const speechRecognition = new window.webkitSpeechRecognition()
      speechRecognition.lang = "ja-JP";
      speechRecognition.continuous = true;
      this.recognition = speechRecognition;
      this.recognition.onstart = () => {
        this.recognitionText = "音声入力中...";
      };
      this.recognition.onend = () => {
        this.recognitionText = "カテゴリーを選ぶ";
      };
      this.recognition.onresult = event => {
        if (event.results.length > 0) {
          this.text = event.results[0][0].transcript;
        }
        this.recognition.stop()
      };
      await this.startTalk()
      this.recognition.start()
    },
    methods:{
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      async startSpeech() {
        await this.recognition.start()
      },
      startTalk: function() {
        for(var index in this.manuscript){
          let welcome = new SpeechSynthesisUtterance();
          welcome.lang = 'ja-JP';
          welcome.rate = 1.3
          welcome.text = this.manuscript[index];
          this.speech.speak(welcome);
        }
        this.isSpaking = this.speech.speaking
      },
    },
    watch:{
      text(val){
        if(val.match(/腫瘍/)){
          val = "主要"
        }
        else if(val.match(/it/ )){
          val = "IT"
        }
        else if(val.match(/社会/ && val.match(/暮らし/))){
          val = "社会・くらし"
        }
        else if(val.match(/社会/ && val.match(/暮らし/))){
          val = "社会・くらし"
        }
        else if(val.match(/エンタメ/ && val.match(/文化/))){
          val = "エンタメ・文化"
        }
        else if(val.match(/囲碁/ && val.match(/将棋/))){
          val = "囲碁・将棋"
        }
        if(this.category_dict[val]){
          this.speech.cancel()
          localStorage.category = val
          localStorage.category_url = this.category_dict[val]
          this.$router.push('./news-list')
        }else{
          this.speech.cancel()
          let u = new SpeechSynthesisUtterance();
          u.lang = 'ja-JP';
          u.rate = 1.3
          u.text = 'もう一度お願いします。' + val + "と聞こえました。";
          this.speech.speak(u);
        }
      }
    }

  }
</script>

<style scoped lang="scss">
.title{
  font-size: 4em !important;
  line-height: 1em !important;
}

.speak{
  font-size: 2em !important;
  line-height: 1.5em !important;
  margin-bottom: 0.8em !important;

}

.v-btn__content{
  font-size: 2em !important;
}

.regnitional-btn{
  height: 100px !important;
  min-width: 94px !important;
  font-size: 3em !important;
  padding: 0.5em !important;
}

@media screen and (min-width:480px) and (max-width:768px) {
  .title{
    font-size: 3em !important;
    line-height: 1em !important;
  }
}

@media screen and (max-width:480px)  {
  .title{
    font-size: 2em !important;
    line-height: 1em !important;
  }
}
</style>
