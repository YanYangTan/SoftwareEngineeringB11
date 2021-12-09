<template>
  <div class="container">
    <div>
      <h2>Multiple File</h2>
      <hr/>
      <label>Files
        <input type="file" id="files" ref="files" multiple v-on:change="handleFileUpload( $event )"/>
      </label>
      <label>User_ID
        <input type="number" v-model="user_id"/>
      </label>
      <label>Group_ID
        <input type="number" v-model="group_id"/>
      </label>
      <label>Caption
        <input type="text" v-model="caption"/>
      </label>
      <br>
      <button v-on:click="SubmitFile()">Submit</button>
    </div>
    <button v-on:click="getPic()">Get Picture</button>
    <img :src="picurl"/>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Upload',
  data() {
    return {
      files: '',
      user_id: '',
      group_id: '',
      caption: '',
      picurl: '',
    };
  },
  methods: {
    getPic() {
      axios({
        method: 'get',
        url: '/api/get-image',
        responseType: 'arraybuffer',
      }).then((res) => {
        // eslint-disable-next-line prefer-template
        this.picurl = 'data:image/jpeg;base64,' + this.arrayBufferToBase64(res.data);
      });
    },
    arrayBufferToBase64(buffer) {
      let binary = '';
      const bytes = new Uint8Array(buffer);
      const len = bytes.byteLength;
      for (let i = 0; i < len; i += 1) {
        binary += String.fromCharCode(bytes[i]);
      }
      return window.btoa(binary);
    },
    handleFileUpload() {
      // eslint-disable-next-line prefer-destructuring
      this.files = this.$refs.files.files;
    },
    SubmitFile() {
      // eslint-disable-next-line prefer-const
      let formData = new FormData();
      // eslint-disable-next-line vars-on-top
      for (let i = 0; i < this.files.length; i += 1) {
        const file = this.files[i];
        // eslint-disable-next-line prefer-template
        formData.append('files[]', file);
      }
      formData.append('user_id', this.user_id);
      formData.append('group_id', this.group_id);
      formData.append('caption', this.caption);
      axios.post('/api/upload-post',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          // eslint-disable-next-line prefer-arrow-callback
        }).then((res) => {
        if (res.data.status) {
          console.log('Success');
        }
      })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
