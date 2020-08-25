<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">{{site}} : {{ category }}</h1>

        <p class="speak mt-10">読みたいニュースを選んでください。選択は１番のように選択してください</p>
        <v-list class='mx-auto text-center' >
          <v-list-item
            class='text-center'
            v-for="(news, i) in newsList"
            :key="i"
          >
            <v-list-item-title class='news_title mb-4'>{{i + 1}}.  {{news.name}}</v-list-item-title>
          </v-list-item>
        </v-list>       
        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
        <button @click="startTalk" class='read'>音声読み上げ</button>
        <p>{{ text }}</p>
      </v-col>
      
    </v-row>
  </v-container>
</template>

<script>
  export default {
    data(){
      return {
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        newsList: [
          {name: '東京都内で新たに１８２人感染確認…２日連続で２００人下回る', id: '20200825-OYT1T50276' },
          {name: '東京都内で新たに１８２人感染確認…２日連続で２００人下回る', id: '20200825-OYT1T50276' }
        ],
        site: localStorage.getItem("site"),
        category: localStorage.getItem("category"),
        show: false
      }
    },
    async mounted(){
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
        welcome.text = this.site + 'の'  + this.category + 'です。';
        speechSynthesis.speak(welcome);
        this.sleep(1)
        let news = new SpeechSynthesisUtterance();
        news.lang = 'ja-JP';
        news.rate = 1.3
        news.text = '読みたいニュースを選んでください。選択は番号でお願いします。';
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
        const val_list = val.split('番')
        localStorage.newsId = this.newsList[Number(val_list[0])].id
        this.$router.push('./news')
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

.news_title{
  font-size: 2em !important;
  line-height: 1.5em !important;
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