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
        
        <h1 class="title mt-10">{{title}}</h1>

        <p class="speak mt-10">要約文</p>
        <!-- <p> {{ news }}</p> -->
        <p class="speak mt-10" v-for='row in content' :key="row">
          <span v-for='word in row' :key="word" :class='calcHot(word)'>
            {{ word}}
          </span>
          
        </p>

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
        isLoading: true,
        fullPage: true,
        recognition : "",
        recognitionText: "音声入力開始",
        text: "",
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        abst: '明日は京都に行きたいと思ってます',
        site: localStorage.getItem("site"),
        title: localStorage.getItem("newsTitle"),
        titleUrl: localStorage.getItem("newsUrl"),
        fee: localStorage.getItem("newsFee"),
        manuscript: [],
        show: false,
        news: {},
        content: [],
        regular_expresion: "",
        reccomendscript: '何か気になった単語はありましたか？。オススメの関連ニュースを読みますか？。回答は、単語を調べる、関連ニュースを読むのどちらかでお願いします。',
        recommend: []
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + "/api/summarize", {params: { "media": this.site_dict[this.site], "url": this.titleUrl} })
        .then(response => {
          console.log(response.data)
          this.manuscript.push("タイトル、" + this.title)
          this.news = response.data
          this.manuscript.push("要約、")
          for(var index in response.data.summary) {
            this.manuscript.push(response.data.summary[index])
          }
          this.regular_expresion = new RegExp('(' + response.data.ne_list.join('|') + ')', 'i');
        }).catch(error => {
          console.log(error)
      })

      for(var row in this.news.summary){
        this.content.push( this.news.summary[row].split(this.regular_expresion) )
      }

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
      // recognition.start()
      this.isLoading = false
    },
    methods:{
      sleep(waitMsec) {
        window.setTimeout(() => {},waitMsec)
      },
      calcHot(word){
        if(this.news.ne_list.indexOf(word) !== -1){
          if(this.news.trends[word] > 500){
            return ['large_word']
          }else if(this.news.trends[word] > 300){
            return ['midle_word']
          }else if(this.news.trends[word] > 100){
            return ['small_word']
          }
          
        }
        return []
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
          this.$router.push('./words')
        }
        else if(this.text.match(/単語/)){
          this.$router.push('./recommend')
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