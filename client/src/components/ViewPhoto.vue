<template>
  <el-container style="margin-top: -7px">
  <div>
    <el-container style="margin-bottom: 4px">
    <el-button
      style="margin-bottom: 10px" size="medium"
      icon="el-icon-back"
      @click="BackToImageWall"
    type="primary">回到照片墙</el-button>
    </el-container>
    <el-container>
 <el-aside width="1090px">
   <el-card :body-style="{ padding: '10px' }" shadow="hover">
     <el-image
      :src="info.src"
      :preview-src-list="[info.src]">
    </el-image>

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
            <el-row>
              <h2 style="margin-top: 12px;margin-left: 5px">{{this.$props.info.caption}}</h2>
            </el-row>

    <el-row :gutter="20">
            <el-table
      :data="commentList"
      style="width: 100%">
      <el-table-column prop="username"
        label="Username"
        width="100">
      </el-table-column>

      <el-table-column prop="content" label="Comments" width="400">
        <template slot-scope="scope">
          <p>{{ scope.row.content }}</p>
          <div slot="reference" class="name-wrapper">
            <el-button
                style="margin-left: 0px"
                size="mini" type='danger' icon="el-icon-delete"
                @click="deleteComment(scope.$index, scope.row)"
                v-if="matchStateDeleted(scope.row)"></el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    </el-row>

            <el-row :gutter="20">
            <el-input placeholder="写个评论吧！" v-model="comment"></el-input></el-row>
            <div>
            <el-button type="primary" icon="el-icon-edit" @click="addComment" style="padding: 10px 10px;">Comment</el-button>
             <el-button type="success"
                size="default"
                icon="el-icon-star-on"
                style="padding: 10px 10px;"
                @click="like()"
              >Like  {{this.likes}}</el-button></div>
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
      comment: '',
      imagelist: [],
      srcList: [],
      picData: {},
      commentList: {},
      likes: '',
      DeleteVisible: false,
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
        like() {
          axios.post('/api/query-like', { post_id: this.$props.info.post_id, user_id: this.$route.params.userid }).then((res) => {
            if (res.data.status) {
              if (res.data.liked) {
                axios.post('/api/cancel-like', { post_id: this.$props.info.post_id, user_id: this.$route.params.userid }).then((res2) => {
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
                axios.post('/api/like-post', { post_id: this.$props.info.post_id, user_id: this.$route.params.userid }).then((res2) => {
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
          axios.post('/api/query-post', { post_id: this.info.post_id }).then((res) => {
            if (res.data.status) {
              this.likes = res.data.content.like;
            }
          });
          console.log('getPost');
          this.likes = this.info.like;
          // axios.post('/api/query-all-post', { group_id: this.$props.info.id }).then((res) => {
          //   let posts = [];
          //   if (res.data.status) {
          //     posts = res.data.post_list;
          //     console.log(posts);
          //     for (let i = 0; i < posts.length; i += 1) {
          //       // eslint-disable-next-line
          //       const src = '/api/show/' + this.$props.info.id + '/' + posts[i].media;
          //       const tmp = {};
          //       tmp.src = src;
          //       tmp.post_id = posts[i].id;
          //       tmp.caption = posts[i].caption;
          //       tmp.date_created = posts[i].date_created;
          //       tmp.like = posts[i].like;
          //       tmp.user_id = posts[i].user_id;
          //       tmp.username = posts[i].username;
          //       this.imagelist.push(tmp);
          //       this.srcList.push(src);
          //     }
          //     console.log(this.imagelist);
          //     this.fullscreenLoading = false;
          //   }
          // }).catch((err) => {
          //   console.log(err);
          // });
          axios.post('/api/query-comment', { post_id: this.info.post_id }).then((res) => {
            let comments = [];
            if (res.data.status) {
              comments = res.data.comments_list;
              this.commentList = comments;
              // console.log('comments');
              // console.log(comments);
              this.comment = '';
              // console.log(this.$props.info.like);
            }
          });
        },
        addComment() {
          axios.post('/api/add-comment', { post_id: this.info.post_id, user_id: this.$route.params.userid, content: this.comment }).then((res) => {
            if (res.data.status) {
              console.log('Comment posted');
              this.getPost();
            }
          });
        },
        deleteComment(index, row) {
          console.log(row.id);
          axios.post('/api/delete-comment', { comment_id: row.id, user_id: Number(this.$route.params.userid) }).then((res) => {
            if (res.data.status) {
              console.log('delete success');
              this.getPost();
            } else {
              console.log(res.data.message);
            }
          });
        },
        matchStateDeleted(row) {
          return this.DeleteVisible && (Number(row.user_id) === Number(this.$route.params.userid));
        },
        deleteCheck() {
          if (this.DeleteVisible === true) {
            this.DeleteVisible = false;
          } else {
            this.DeleteVisible = true;
          }
        },
      },
  created() {
    console.log('success!');
    // this.data = this.info;
    this.getPost();
    this.deleteCheck();
  },
};
</script>

<style scoped>
  .el-image {
    width: 100%;
    object-fit: scale-down;
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
</style>
