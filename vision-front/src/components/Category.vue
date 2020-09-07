<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        
        <h1 class="title mt-10">{{site}}</h1>

        <p class="speak mt-10">読みたいカテゴリーを選んでください。</p>
        <p class="speak ">カテゴリーは{{ categorys }}があります。</p>
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
        recognitionText: "カテゴリーを選ぶ",
        text: "",
        site_dict: {"ヤフーニュース":0, "朝日新聞":1, "読売新聞":2, "日経新聞":3},
        site: localStorage.getItem("site"),
        category_dict: {},
        manuscript: [],
        categorys: "",
        show: false
      }
    },
    async mounted(){
      await axios
        .get(process.env.VUE_APP_API + ":8000/api/category", {params: { "media": this.site_dict[this.site] }})
        .then(response => {
          this.manuscript.push(this.site + 'で読めるカテゴリーは、')
          this.category_list = response.data
          for(let key in response.data){
            this.categorys += key + "、"
            if(key.match(/IT/)){
              key = key.replace('IT','アイティー')
            }
            this.manuscript.push(key)
          }
          this.manuscript.push("があります。")
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
        this.recognitionText = "カテゴリーを選ぶ";
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
      speech(val){
        let welcome = new SpeechSynthesisUtterance();
        welcome.lang = 'ja-JP';
        welcome.rate = 1.3
        welcome.text = val;
        speechSynthesis.speak(welcome);
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
        if(val.match(/it/)){
          val = "IT"
        }
        if(this.category_list[val]){
          localStorage.category = val
          localStorage.category_url = this.category_list[val]
          this.$router.push('./news-list')
        }else{
          console.log(val)
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