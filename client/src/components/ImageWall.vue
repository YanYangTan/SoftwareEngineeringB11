<template>
  <div>
    <div>
      <h2>Multiple File</h2>
      <hr/>
      <label>Files
        <input type="file" id="files" ref="files" multiple v-on:change="handleFileUpload( $event )"/>
      </label>
      <label>Caption
        <input type="text" v-model="caption"/>
      </label>
      <br>
      <el-button v-on:click="SubmitFile()">Submit</el-button>
    </div>
    <el-row :gutter="20" v-loading.fullscreen.lock="fullscreenLoading">
          <el-col :span="4" v-for="item in imagelist" :key="item.post_id" style="height:250px">
            <el-card :body-style="{ padding: '0px 0px' }">
              <div slot="header">
                <el-image
      style="width: auto; height: 160px"
      :src="item.src"
      :preview-src-list="srcList">
    </el-image>
  </div>
              <el-button type="success"
                size="mini"
                icon="el-icon-arrow-up"
                style="padding: 1px 1px;"
                @click="like(item)"
              >{{item.like}}</el-button>
              <el-button
                size="mini"
                icon="el-icon-edit-outline"
                style="padding: 1px 2px;"
                type="text"
                class="button"
                @click="viewPhoto(item)"
              >详情</el-button>
            </el-card>
          </el-col>
        </el-row>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ImageWall',
  data() {
    return {
      files: '',
      caption: '',
      fullscreenLoading: true,
      imagelist: [],
      showViewer: false,
      view_index: 0,
      srcList: [],
      comments: [],
      likeCount: [],
    };
  },
  props: {
    info: {},
  },
  methods: {
    getPost() {
      this.imagelist = [];
      this.srcList = [];
      this.fullscreenLoading = true;
      axios.post('/api/query-all-post', { group_id: this.$props.info.id })
        .then((res) => {
          let posts = [];
          if (res.data.status) {
            posts = res.data.post_list;
            console.log(posts);
            for (let i = 0; i < posts.length; i += 1) {
              // eslint-disable-next-line
              const src = '/api/show/' + this.$props.info.id + '/' + posts[i].media;
              const tmp = {};
              tmp.src = src;
              tmp.post_id = posts[i].id;
              tmp.caption = posts[i].caption;
              tmp.date_created = posts[i].date_created;
              tmp.like = posts[i].like;
              this.likeCount[i] = tmp.like;
              tmp.user_id = posts[i].user_id;
              tmp.username = posts[i].username;
              this.imagelist.push(tmp);
              this.srcList.push(src);
            }
            console.log(this.imagelist);
            this.fullscreenLoading = false;
            console.log('like count here');
            console.log(this.likeCount);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    like(pic) {
      axios.post('/api/query-like', { post_id: pic.post_id, user_id: this.$route.params.userid })
        .then((res) => {
          if (res.data.status) {
            if (res.data.liked) {
              axios.post('/api/cancel-like', { post_id: pic.post_id, user_id: this.$route.params.userid })
                .then((res2) => {
                  if (res2.data.status) {
                    this.$message({
                      type: 'warning',
                      message: '你已点赞此帖，取消点赞',
                    });
                    this.getPost();
                  }
                })
                .catch((err2) => {
                  console.log(err2);
                });
            } else {
              axios.post('/api/like-post', { post_id: pic.post_id, user_id: this.$route.params.userid })
                .then((res2) => {
                  if (res2.data.status) {
                    console.log('Liked');
                    this.$message({
                      type: 'success',
                      message: '成功点赞',
                    });
                    this.getPost();
                  }
                })
                .catch((err2) => {
                  console.log(err2);
                });
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    viewPhoto(item) {
      this.$emit('viewPhoto', item);
      // axios.post('/api/query-comment', { post_id: pic.post_id })
      //   .then((res) => {
      //     if (res.data.status) {
      //       this.comments = res.data.comments_list;
      //       console.log(this.comments);
      //     }
      //   })
      //   .catch((err) => {
      //     console.log(err);
      //   });
    },
    handleFileUpload() {
      // eslint-disable-next-line prefer-destructuring
      this.files = this.$refs.files.files;
    },
    SubmitFile() {
      this.fullscreenLoading = true;
      // eslint-disable-next-line prefer-const
      let formData = new FormData();
      // eslint-disable-next-line vars-on-top
      for (let i = 0; i < this.files.length; i += 1) {
        const file = this.files[i];
        // eslint-disable-next-line prefer-template
        formData.append('files[]', file);
      }
      formData.append('user_id', this.$route.params.userid);
      formData.append('group_id', this.$props.info.id);
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
          this.$message({
            type: 'success',
            message: '成功上传',
          });
          this.getPost();
        }
      })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.getPost();
  },
};
</script>

<style scoped>

</style>
