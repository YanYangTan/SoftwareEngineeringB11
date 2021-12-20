<template>
  <div>
     <el-card>
  <el-table
    :data="tableData.filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
    max-height="100%"
    :row-class-name="tableRowClassName"
  v-loading="loading">
<!--    style="width: 100%;margin-bottom: 20px;"-->
<!--  v-loading="loading">-->
    <el-table-column
      label="成员"
      prop="username"
    width="110px">
    </el-table-column>
    <el-table-column
      align="right">
      <template slot="header" slot-scope={}>
        <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
      </template>
      <template slot-scope="scope">
        <el-button size="mini" @click="openProfileBubble(scope.$index,scope.row)" type="info">详情</el-button>
        <el-dialog
  title=" "
  :visible.sync="dialogVisible"
  width="50%">
          <span>
  <el-descriptions title="User Info"
  v-loading="loading">
    <el-descriptions-item label="Username">{{ username }}</el-descriptions-item>
    <el-descriptions-item label="Telephone">{{phone}}</el-descriptions-item>
    <el-descriptions-item label="Birthday">{{ birthday }}</el-descriptions-item>
    <el-descriptions-item label="Quote">{{quote}}</el-descriptions-item>
  </el-descriptions></span>
  <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogVisible = false">Confirm</el-button>
  </span>
</el-dialog>

        <el-button
          size="mini"
          type="danger"
          v-if="matchStateDelete(scope.row)"
          @click="handleDelete(scope.$index,scope.row)">移除</el-button>
        <el-button
          size="mini"
          type="primary"
          v-if="matchState(scope.row)"
          @click="handleSetAdmin(scope.$index,scope.row)">设置</el-button>
        <el-button
          size="mini"
          type="warning"
          v-if="matchStateA(scope.row)"
          @click="handleRemoveAdmin(scope.$index,scope.row)">回收</el-button>
      </template>
    </el-table-column>
  </el-table>
       <el-button v-if="this.$props.info.admin" style="color: crimson;margin-top: 10px" @click="EditAdminClick">{{adminbutton}}</el-button>
    <el-button v-if="this.$props.info.admin" style="color: crimson;margin-top: 10px" @click="EditClick">{{editbutton}}</el-button>
   </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      editA: false,
      adminbutton: '设置群主',
      loading: true,
      tableData: [],
      search: '',
      edit: false,
      editbutton: '编辑',
      dialogVisible: false,
      id: '',
      birthday: '',
      email: '',
      message: '',
      phone: '',
      username: '',
      quote: '',
    };
  },
  props: {
    // eslint-disable-next-line vue/require-prop-type-constructor
    info: {},
  },
  methods: {
    handleSetAdmin(index, row) {
      axios.post('/api/set-admin', { group_id: this.$props.info.id, user_id: row.id })
        .then((res) => {
          if (res.data.status) {
            // this.$data.tableData = res.data.user_list;
            this.$data.tableData[index].admin = true;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    handleRemoveAdmin(index, row) {
      axios.post('/api/remove-admin', { group_id: this.$props.info.id, user_id: row.id })
        .then((res) => {
          if (res.data.status) {
            // this.$data.tableData = res.data.user_list;
            this.$data.tableData[index].admin = false;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    matchStateDelete(row) {
      return this.edit && (Number(row.id) !== Number(this.$route.params.userid));
    },
    matchState(row) {
      return this.editA && (!row.admin);
    },
    matchStateA(row) {
      return this.editA && (row.admin) && (Number(row.id) !== Number(this.$route.params.userid));
    },
    tableRowClassName({ row }) {
      if (row.admin) {
        return 'admin-row';
      }
      return 'else-row';
    },
    handleEdit(index, row) {
      console.log(row);
      // row.id
    },
    openProfileBubble(index, row) {
      // this.handleEdit(this.scope.$index, this.scope.row);
      this.loading = true;
      this.dialogVisible = true;
      this.id = row.id;
      console.log(row.id);
      console.log(this.id);
      axios.post('/api/query-userinfo', { user_id: this.id })
        .then((res) => {
          if (res.data.status) {
            console.log('Query success!');
            this.birthday = res.data.birthday;
            this.email = res.data.email;
            this.phone = res.data.phone;
            this.username = res.data.username;
            this.quote = res.data.quote;
            this.loading = false;
          } else {
            console.log(res.data.message);
          }
        });
    },
    handleDelete(index, row) {
      axios.post('/api/remove-member', { group_id: this.$props.info.id, user_id: row.id })
        .then((res) => {
          if (res.data.status) {
            // this.$data.tableData = res.data.user_list;
            this.$data.tableData.splice(index, 1);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    EditAdminClick() {
      if (this.editA) {
        this.editA = false;
        this.adminbutton = '设置群主';
      } else {
        this.editA = true;
        this.adminbutton = '设置完毕';
      }
    },
    EditClick() {
      if (this.edit) {
        this.edit = false;
        this.editbutton = '编辑';
      } else {
        this.edit = true;
        this.editbutton = '编辑完毕';
      }
    },
    getUser() {
      this.loading = true;
      axios.post('/api/query-user', { group_id: this.$props.info.id })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            this.$data.tableData = res.data.user_list;
            console.log(res.data.user_list);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created() {
    this.getUser();
  },
};
</script>
<style>
.el-table .admin-row {
    background: #f0f9eb;
  }
/*.el-table__body-wrapper::-webkit-scrollbar{*/
/*     !*width: 0;宽度为0隐藏*!*/
/*    width: 2px;*/
/*  }*/
/* .el-table__body-wrapper::-webkit-scrollbar-thumb{*/
/*    border-radius: 2px;*/
/*    height: 50px;*/
/*    background: #eee;*/
/*  }*/
/* .el-table__body-wrapper::-webkit-scrollbar-track{*/
/*    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);*/
/*    border-radius: 2px;*/
/*    background: rgba(0,0,0,0.4);*/
/*  }*/
</style>
