<template>
  <div>
  <el-table
    :data="tableData.filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%">
    <el-table-column
      label="Name"
      prop="username">
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
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">详情</el-button>
        <el-button
          size="mini"
          type="danger"
          v-if="edit"
          @click="handleDelete(scope.$index,scope.row)">移除</el-button>
      </template>
    </el-table-column>
  </el-table>
    <el-button v-if="this.$props.info.admin" style="color: crimson" @click="EditClick">{{editbutton}}</el-button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tableData: [],
      search: '',
      edit: false,
      editbutton: '编辑',
    };
  },
  props: {
    // eslint-disable-next-line vue/require-prop-type-constructor
    info: {},
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
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
      axios.post('/api/query-user', { group_id: this.$props.info.id })
        .then((res) => {
          if (res.data.status) {
            this.$data.tableData = res.data.user_list;
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
