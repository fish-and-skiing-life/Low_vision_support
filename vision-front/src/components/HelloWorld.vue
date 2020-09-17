<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">Wellcome to<br> Low vision service</h1>

        <p class="speak mt-10">読みたいニュースサイトを選んでください。</p>
        <p class="speak ">ニュースサイトは、ヤフーニュース、朝日新聞、読売新聞、日経新聞を利用できます。</p>
        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
      </v-col>
      
    </v-row>
  </v-container>
</template>

<script>
  export default {

    data(){
      return {
        speech: window.speechSynthesis,
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        show: false,
        intervalID: ''
      }
    },
    async mounted(){
      await this.getVoice().then(response => {
        this.voice = response[57]
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
        // this.recognition.stop()
      };
      await this.startTalk()
      recognition.start()

    },
    methods:{
      getVoice(){
        let intervalId;
        return new Promise((resolve) => {
          setInterval(() =>{
            if(this.speech.getVoices().length > 0){
              resolve(this.speech.getVoices())
              clearInterval(intervalId)
            }
          }, 10)
        })
      },
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      async startSpeech() {
        await this.recognition.start()
      },
      startTalk(){
        let welcome = new SpeechSynthesisUtterance();
        welcome.lang = 'ja-JP';
        welcome.rate = 1.3
        welcome.text = 'ようこそ! low vision webアプリケーションへ。';
        this.speech.speak(welcome);
        let news = new SpeechSynthesisUtterance();
        news.lang = 'ja-JP';
        news.rate = 1.3
        news.text = '読みたいニュースサイトを選んでください。';
        this.speech.speak(news);

        let u = new SpeechSynthesisUtterance();
        u.lang = 'ja-JP';
        u.rate = 1.3
        u.text = 'ニュースサイトは、ヤフーニュース、朝日新聞、読売新聞、日経新聞を利用できます。';
        this.speech.speak(u);

      },
    },
    watch:{
      text(val){
        var exist = true
        if (val.match(/Yahoo/)) {
          localStorage.site = 'ヤフーニュース'
        }else if(val.match(/朝日新聞/)){
          localStorage.site = '朝日新聞'
        }
        else if(val.match(/読売新聞/)){
          localStorage.site = '読売新聞'  
        }
        else if(val.match(/日経新聞/)){
          localStorage.site = '日経新聞'
        }
        else{
          exist = false
        }

        if( exist){
          this.speech.cancel()
          this.$router.push('./category')
        }else{
          this.speech.cancel()
          let u = new SpeechSynthesisUtterance();
          u.lang = 'ja-JP';
          u.rate = 1.3
          u.text = 'もう一度お願いします。' + val + "と聞こえました。";
          speechSynthesis.speak(u);
        }
        
      },
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