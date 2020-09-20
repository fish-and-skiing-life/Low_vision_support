<template>
  <div>
    <loading 
      :active.sync="isLoading" 
      :is-full-page="fullPage"
      background-color='#000'
      color= '#fff'
      :height= '150'
      :width ="150"
      :opacity='0.8'
      loader = "bars"
      >  
    </loading>
  <v-container>
    

    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">気になった単語 : {{ word }} </h1>
        <p class="speak mt-10"> wikipedia 概要の要約 </p>
        <p class="speak mt-10" v-for='row in summary' :key="row">{{ row }}</p>

        <v-btn x-large color="primary" @click="startSpeech">{{ recognitionText }}</v-btn><br>
        <button @click="startTalk" class='read'>音声読み上げ</button>
        <p>{{ text }}</p>
      </v-col>
      
    </v-row>
  </v-container>
</div>
</template>

<script>
  import Loading from 'vue-loading-overlay';
  import 'vue-loading-overlay/dist/vue-loading.css';
  import axios from 'axios';
  export default {
    components: {
      Loading
    },
    data(){
      return {
        speech: window.speechSynthesis,
        isLoading: true,
        fullPage: true,
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        manuscript: [],
        data: {},
        summary: []
      }
    },
    async mounted(){
      this.manuscript.push('気になった単語を教えてください。')

      const speechRecognition = new window.webkitSpeechRecognition()
      speechRecognition.lang = "ja-JP";
      speechRecognition.continuous = true;
      this.recognition = speechRecognition;
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
      this.recognition.start()
      await this.startTalk()
      this.isLoading = false
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
          speechSynthesis.speak(welcome);
          this.sleep(1)
        }

      },
    },
    watch:{
      text(val){
        if (this.text.match(/関連ニュース/)) {
          this.speech.cancel()
          this.$router.push('./recommend_list')
        }
        else if(this.text.match(/単語/)){
          this.speech.cancel()
          this.$router.push('./wiki')
        }else{
          console.log(val)
          this.isLoading = true
          axios
            .get(process.env.VUE_APP_API + "/api/wiki", {params: { "word": val} })
            .then(response => {
              console.log(response.data)
              this.word = val
              this.data = response.data
              if(response.data.title == 'error'){
                this.manuscript = [val + 'は、Wikipediaにありませんでした。他の単語を調べてください。']
                this.startTalk()
              }else{
                this.summary = response.data.summary
              }
              
              this.isLoading = false
            }).catch(error => {
              console.log(error)
          })
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
  line-height: 1.7em !important;
  margin-bottom: 0.8em !important;

}

.large_word{
  font-size: 2.3em !important;
  font-weight: bold;
  line-height: 1.4em !important;
}

.midle_word{
  font-size: 1.6em !important;
  line-height: 1.2em !important;
}

.small_word{
  font-size: 1.3em !important;
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
