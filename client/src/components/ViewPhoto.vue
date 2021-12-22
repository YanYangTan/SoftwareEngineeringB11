<template>
  <el-container style="margin-top: -7px">
  <div>
    <el-container style="margin-bottom: 4px">
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToImageWall" circle
    type="primary"></el-button>
    <h1 >{{this.$props.info.caption}}</h1>
    </el-container>
    <el-container>
 <el-aside width="900px">
   <el-card :body-style="{ padding: '10px' }" shadow="hover">
     <el-image
      :src="info.src"
      :preview-src-list="[info.src]">
    </el-image>
                   <el-button type="success"
                size="large"
                icon="el-icon-arrow-up"
                style="padding: 1px 1px;"
                @click="like(info.like)"
              >{{info.like}}</el-button>
   </el-card>
 </el-aside>
      <el-container>

      <el-main>
        <div>
          <el-card >
            <el-container>
         <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                 style=""  :size="50"></el-avatar>
        <h3 style="margin-top: 12px;margin-left: 5px">
          {{info.username}}
        </h3>
            </el-container>
        <span style="margin-left: 5px">{{info.date_created}}</span>
           </el-card>
        </div>
      </el-main>

    </el-container>
</el-container>
  </div>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewPhoto',
  data() {
    return {
      comment: {},
      imagelist: [],
      srcList: [],
      picData: {},
    };
  },
  props: {
    info: {},
  },
  methods:
      {
        BackToImageWall() {
          this.$emit('BacktoImageWall');
        },
        like(pic) {
          axios.post('/api/query-like', { post_id: pic.post_id, user_id: this.$route.params.userid }).then((res) => {
            if (res.data.status) {
              if (res.data.liked) {
                axios.post('/api/cancel-like', { post_id: pic.post_id, user_id: this.$route.params.userid }).then((res2) => {
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
                axios.post('/api/like-post', { post_id: pic.post_id, user_id: this.$route.params.userid }).then((res2) => {
                  if (res2.data.status) {
                    console.log('Liked');
                    this.$message({
                      type: 'success',
                      message: '成功点赞',
                    });
                    this.getPost();
                  }
                }).catch((err2) => {
                  console.log(err2);
                });
              }
            }
          }).catch((err) => {
            console.log(err);
          });
        },
        getPost() {
          this.picData = this.info;
          console.log(this.picData);
          axios.post('/api/query-all-post', { group_id: this.$props.info.id }).then((res) => {
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
                tmp.user_id = posts[i].user_id;
                tmp.username = posts[i].username;
                this.imagelist.push(tmp);
                this.srcList.push(src);
              }
              console.log(this.imagelist);
              this.fullscreenLoading = false;
            }
          }).catch((err) => {
            console.log(err);
          });
          axios.post('/api/comment', { post_id: this.picData.post_id }).then((res) => {
            let comments = [];
            if (res.data.status) {
              comments = res.data.comments_list;
              console.log(comments);
            }
          });
        },
      },
  created() {
    console.log('success!');
    // this.data = this.info;
    console.log(this.info);
  },
};
</script>

<style scoped>
  .el-image {
    width: 100%;
    object-fit: scale-down;
  }
</style>
