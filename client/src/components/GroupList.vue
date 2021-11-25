<template>
  <div>
    <el-button class="el-icon-circle-plus" @click="createGroup"> 创建群组</el-button>
    <el-button class="el-icon-connection" @click="joinGroup"> 加入群组</el-button>
    <div class="group-list">

      <el-row :gutter="20">
        <el-col :span="4" v-for="item in grouplist" :key="item.id" style="height:100px">
          <el-card :body-style="{ padding: '0px 0px' }">
            <img src="../assets/logo.png" style="max-width:100px;height:50px;margin-bottom: 0px;" class="head_audio" />
            <div slot="header"></div>
            <!-- here to fix text -->
            <span style="font-size: 15px;">{{item.name}}</span>
            <el-button size="mini" icon="el-icon-zoom-in" style="padding: 1px 1px;" type="text"
                       class="button" @click="showBig(item)">试听</el-button>
            <el-button size="mini" icon="el-icon-edit-outline" style="padding: 1px 2px;" type="text"
                       class="button" @click="editOne(item)">标注</el-button>
          </el-card>
        </el-col>
      </el-row>

    </div>
  </div>
</template>

<script>

export default {

  name: 'app',
  data() {
    return {
      grouplist: [{ name: 'a' }, { name: 'b' }],
    };
  },
  methods:
    {
      createGroup() {
        this.$prompt('为你的新群取一个好听的名字', '群组创建', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          this.$message({
            type: 'success',
            message: `你的是: ${value}`,
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入',
          });
        });
      },
      joinGroup() {
        this.$prompt('请输入邀请码', '加入群组', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({ value }) => {
          this.$message({
            type: 'success',
            message: `你的: ${value}`,
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入',
          });
        });
      },
    },
};
</script>
<style>
.group-list{
  margin-top: 10px;
}
</style>
