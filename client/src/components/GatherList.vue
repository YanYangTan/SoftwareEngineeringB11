<template>
  <div>
    <el-button  @click="dialogFormVisible = true">打开嵌套表单的 Dialog</el-button>

<el-dialog title="发起聚会" :visible.sync="dialogFormVisible">
  <el-form :model="temp">
    <el-form-item label="聚会名称" :label-width="formLabelWidth">
      <el-input v-model="gathering.name" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="描述" :label-width="formLabelWidth">
      <el-input v-model="gathering.description" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="截止时间">
    <el-date-picker
      v-model="gathering.enddate"
      type="datetime"
      placeholder="选择日期时间">
    </el-date-picker>
  </el-form-item>
    <el-form-item label="发起类型" :label-width="formLabelWidth">
      <el-radio-group v-model="gathering.status">
      <el-radio label="提议"></el-radio>
      <el-radio label="投票"></el-radio>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="投票多选" :label-width="formLabelWidth">
       <el-switch v-model="gathering.allow_multiple_vote"></el-switch>
    </el-form-item>
    <el-form-item label="内容" :label-width="formLabelWidth">
  <el-form-item
    v-for="(domain, index) in  gathering.content"
    :label="'方案 ' + index"
    :key="domain.key"
    :rules="{
      required: true, message: '不能为空', trigger: 'blur'
    }"
  >
    <el-col :span="11">
      <el-date-picker
      v-model="domain.time"
      type="datetime"
      placeholder="选择日期时间">
    </el-date-picker>
    </el-col>
    <el-input v-model="domain.location"></el-input><el-button @click.prevent="removeDomain(domain)">删除</el-button>
  </el-form-item>
  <el-form-item>
    <el-button @click="addDomain">新建内容</el-button>
    <el-button @click="resetForm">重置</el-button>
  </el-form-item>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="confirmGathering">确 定</el-button>
  </div>
</el-dialog>
<!--    -->
    <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
  <el-table
    :data="this.gatherlist.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%">
    <el-table-column
      label="截止日期"
      prop="enddate">
    </el-table-column>
    <el-table-column
      label="名字"
    prop="name">
      <template slot-scope="scope">
        <el-popover trigger="hover" placement="top-start" >
          <p>描述: {{ scope.row.description }}</p>
          <div slot="reference" class="name-wrapper">
            <el-tag type='info' size="medium">{{ scope.row.name }}</el-tag>
          </div>
        </el-popover>
      </template>
    </el-table-column>
<!--    <el-table-column-->
<!--      align="right">-->
<!--      <template slot="header" slot-scope={}>-->
<!--      </template>-->
<!--    </el-table-column>-->
    <el-table-column
      prop="status"
      label="标签"
      width="100"
      :filters="[{ text: '投票', value: false }, { text: '提议', value: true }]"
      :filter-method="filterTag"
      filter-placement="bottom-end">
      <template slot-scope="scope">
        <el-tag @click="clicktag()"
          type='primary'
          v-if="scope.row.status" disable-transitions>提议</el-tag>
        <el-tag @click="clicktag()"
          type='success'
          v-else-if="scope.row.status=== false" disable-transitions>投票</el-tag>
      </template>
    </el-table-column>
  </el-table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      gatherlist: [],
      addingcontent: false,
      dialogFormVisible: false,
      gathering: {
        user_id: '',
        group_id: '',
        name: '',
        description: '',
        enddate: '',
        status: '提议',
        allow_multiple_vote: 0,
        content: [{ time: '', location: '' }],
      },
      temp: {
        name: '',
        region: '',
        enddateday: '',
        enddatetime: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
      formLabelWidth: '120px',
      tableData: [{
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄',
        tag: '加',
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1517 弄',
        tag: '投票',
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1519 弄',
        tag: '提议',
      }, {
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1516 弄',
      }],
      search: '',
    };
  },
  props: {
    currentgroup: {},
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    filterTag(value, row) {
      return row.status === value;
    },
    queryAllGathering() {
      axios.post('/api/query-all-gathering', { group_id: this.$props.currentgroup.id })
        .then((res) => {
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;
            // appendTag();
            console.log(this.gatherlist);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    createGathering() {

    },
    addContent() {
      this.addingcontent = true;
    },
    // 内容
    resetForm() {
      this.gathering.content = [{ time: '', location: '' }];
    },
    removeDomain(item) {
      const index = this.gathering.content.indexOf(item);
      if (index !== -1) {
        this.gathering.content.splice(index, 1);
      }
    },
    addDomain() {
      this.gathering.content.push({
        time: '',
        location: '',
        key: Date.now(),
      });
    },
    confirmGathering() {
      this.gathering.group_id = this.$props.currentgroup.id;
      this.gathering.user_id = this.$route.params.userid;
      // this.dateFormatting(this.gathering.enddate);
      this.gathering.enddate = '2021-12-15 20:00:00';
      this.gathering.status = this.gathering.status === '提议';
      axios.post('/api/create-gathering', {
        user_id: this.gathering.user_id,
        group_id: this.gathering.group_id,
        name: this.gathering.name,
        description: this.gathering.description,
        enddate: this.gathering.enddate,
        status: this.gathering.status,
        allow_multiple_vote: this.gathering.allow_multiple_vote,
        content: this.gathering.content,
      })
        .then((res) => {
          if (res.data.status) {
            this.gatherlist = res.data.gathering_list;
            // appendTag();
            this.queryAllGathering();
          } else {
            console.log(res.data.status);
          }
        })
        .catch((err) => {
          console.log(err);
        });
      this.gathering.status = '提议';
    },
    dateFormatting() {
      // eslint-disable-next-line no-unused-expressions,no-param-reassign
      // date.substr(4, 6);
      // console.log(date);
    },
  },
  created() {
    this.queryAllGathering();
  },
};
</script>
