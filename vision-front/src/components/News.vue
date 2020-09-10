<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">{{title}}</h1>

        <p class="speak mt-10">要約文</p>
        <p>{{ abst }}</p>
        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
        <button @click="startTalk" class='read'>音声読み上げ</button>
        <p>{{ text }}</p>
      </v-col>
      
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios';
  export default {
    data(){
      return {
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        abst: '明日は京都に行きたいと思ってます',
        site: localStorage.getItem("site"),
        title: localStorage.getItem("newsTitle"),
        titleUrl: localStorage.getItem("newsUrl"),
        fee: localStorage.getItem("newsFee"),
        show: false
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/summarize", {params: { "media": this.site_dict[this.site], "url": this.titleUrl} })
        .then(response => {
          console.log(response.data)
          this.manuscript.push('現在、' + this.site + 'の' + this.category + 'で読める記事のタイトルは、')
          this.data = response.data
          this.newsList = Object.keys(response.data)
          for (const [index, key] of this.newsList.entries()) {
            this.manuscript.push(String(index + 1) + "番、" + key)
          }

          this.manuscript.push("です。")
        }).catch(() => {
      })
      const recognition = new window.webkitSpeechRecognition()
      recognition.lang = "ja-JP";
      recognition.continuous = true;
      this.recognition = recognition;
      this.recognition.onstart = () => {
        this.recognitionText = "音声入力中...";
      };
      this.recognition.onend = () => {
        this.recognitionText = "音声入力開始";
      };
      this.recognition.onresult = event => {
        if (event.results.length > 0) {
          this.text = event.results[0][0].transcript;
        }
        this.recognition.stop()
      };
    },
    methods:{
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      async startSpeech() {
        await this.recognition.start()
      },
      startTalk: function() {
        let welcome = new SpeechSynthesisUtterance();
        welcome.lang = 'ja-JP';
        welcome.rate = 1.3
        welcome.text = '読みたいカテゴリーを選んでください。';
        speechSynthesis.speak(welcome);
        this.sleep(1)
        let news = new SpeechSynthesisUtterance();
        news.lang = 'ja-JP';
        news.rate = 1.3
        news.text = '読みたいニュースサイトを選んでください。';
        speechSynthesis.speak(news);

        this.sleep(1)
        let u = new SpeechSynthesisUtterance();
        u.lang = 'ja-JP';
        u.rate = 1.3
        u.text = 'ニュースサイトは、Yahooニュース、朝日新聞、読売新聞、日経新聞、ライブドアを利用できます。';
        speechSynthesis.speak(u);

      },
    },
    watch:{
      text(val){
        if (this.text.match(/Yahoo/)) {
          localStorage.site = 'Yahooニュース'
          this.$router.push('./category')
        }
        console.log(val)
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