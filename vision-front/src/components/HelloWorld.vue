<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
        
      </v-col>
      <v-col cols="12">
        <h2>dsafasdfasd</h2>
        <button @click="startSpeech">{{ recognitionText }}</button>
        <button @click="startTalk">{{ recognitionText }}</button>
        <p>{{ text }}</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data(){
      return {
        recognition : "",
        recognitionText: "音声入力開始",
        text: ""
      }
    },
    created(){
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
      };
    },
    methods:{
      startSpeech: function() {
        this.recognition.start()
      },
      startTalk: function() {
        let u = new SpeechSynthesisUtterance();
        u.lang = 'ja-JP';
        u.rate = 1.3
        u.text = 'ようこそ! low vision webアプリケーションへ';
        speechSynthesis.speak(u);
      },
    }
  }
</script>
