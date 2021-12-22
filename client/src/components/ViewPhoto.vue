<template>
  <el-container>
  <div>
    <el-button
      style="width: 50px;margin-right: 30px;"
      icon="el-icon-back"
      @click="BackToImageWall" circle
    type="primary"></el-button>
    <h1>{{this.$props.info.caption}}</h1>
    <el-container>
 <el-aside width="1000px">
   <el-card :body-style="{ padding: '10px' }" shadow="hover">

     <el-image
      style="width: 1000px; height: auto"
      :src="info.src">
    </el-image>

   </el-card>
 </el-aside>
      <el-container>
      <el-header>{{info.date_created}}</el-header>

      <el-main>
        <h3>
          {{info.username}}
        </h3>
      </el-main>
<el-button type="success"
                size="medium"
                icon="el-icon-arrow-up"
                style="padding: 1px 1px;"
                @click="like(this.info)"
              >{{info.like}}</el-button>
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
      data: {},
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
          axios.post('/api/query-all-post', { group_id: this.$props.info.id })
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
