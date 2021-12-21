<template>
  <div id="app">
    <el-card>
            <div>
        <el-button type="danger" icon="el-icon-delete" @click="clearGenealogy">重置家谱</el-button>
        <el-button type="primary" icon="el-icon-check" @click="saveGenealogy">保存家谱</el-button>
      </div>
      <el-button @click="outputUsedtable">test</el-button>
<!--    <div class="text-center">-->
<!--&lt;!&ndash;      <h1 class="title">家谱</h1>&ndash;&gt;-->
<!--    </div>-->
    <VueFamilyTree
      :tree="tree"
      @card-click="cardClick"
    >
      <template
        v-if="customCard"
        v-slot:card="{item}"
      >
        <el-popover
  placement="right"
  width="100"
  trigger="click">
  <el-menu :default-openeds="['2']">
    <el-popover
  placement="right"
  width="100"
  trigger="click">
      <el-menu :default-openeds="['3']">
        <div v-if="item.defined">
        <el-menu-item index="2-1" @click="addMember(item,'Sibling')">兄弟</el-menu-item>
        <el-menu-item index="2-2" @click="addMember(item,'Children')">儿女</el-menu-item>
        <el-menu-item index="2-3" @click="addMember(item,'Honey')">配偶</el-menu-item>
          </div>
        <div v-else v-for="user in userlist" :key="user.id">
<el-menu-item index="4-1" v-if="user.used===false" @click="item.id=user.id;
          item.defined=true;item.name=user.username;item.image='https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png';user.used = true;usedtable.push(user.id)">{{user.username}}</el-menu-item>
        </div>
      </el-menu>
    <el-menu-item  v-if="item.defined" slot="reference" index="3-2">添加成员</el-menu-item>
      <el-menu-item  v-if="!item.defined" slot="reference" index="3-3">选择成员</el-menu-item>
    </el-popover>
            <el-popover
  placement="right"
  v-model="seeable"
  width="300"
  trigger="click">
              <el-menu>
              <el-menu-item index="4-1" >
                <el-input v-model="nameinput" placeholder="请输入内容"></el-input>
                <el-button @click="customizeName();
                     item.defined=true;
                     item.name=nameinput;
                     item.image='https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
                     seeable=false;
                     "
                >确定</el-button>
              </el-menu-item>
                </el-menu>
                          <el-menu-item  v-if="!item.defined"
                     slot="reference"
                     index="3-4">自定义成员</el-menu-item>
                            </el-popover>
    <el-menu-item index="2-4" style="color: red" @click="addMember(item,'Delete')">删除</el-menu-item>
  </el-menu>
        <el-button slot="reference" class="custom-card"  @click="cardClick(item)">
          <div
            :style="{backgroundImage: item.image ? `url(${item.image})` :  null}"
            class="custom-card__image"
          />
          <div class="custom-card__info">
            <div class="custom-card__name">
              {{ item.name }}
            </div>
            <div
              v-show="item.age"
              class="custom-card__age"
            >
              Age: {{ item.age }}
            </div>
          </div>
        </el-button>
        </el-popover>
      </template>
    </VueFamilyTree>
      </el-card>
  </div>
</template>

<script>
import VueFamilyTree from 'vue-family-tree';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    VueFamilyTree,
  },
  props: {
    // eslint-disable-next-line vue/require-prop-type-constructor
    info: {},
  },
  data() {
    return {
      customCard: true,
      usedtable: [],
      seeable: false,
      userlist: [],
      nameinput: '',
      randomnum: 0,
      temptree: [],
      currentchildren: [],
      currentnode: {},
      minus: -1,
      uppertree: [],
      tree: [{
        firstPerson: {
          name: '未定义',
          image: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          id: -1,
          defined: false,
          used: false,
          root: true,
        },
      }],
    };
  },
  methods: {
    cardClick(item) {
      console.log(item);
    },
    // 添加成员
    addMember(item, type) {
      console.log(item);
      this.test(this.tree, item.id); // 返回选中节点和层的信息
      if (type === 'Sibling') {
        console.log('addSibling');
        // eslint-disable-next-line no-restricted-syntax
        const ele = { firstPerson: { name: '未定义', id: this.minus, image: 's' } };
        this.minus -= 1;
        this.currentchildren.push(ele);
      } else if (type === 'Children') {
        const ele = { firstPerson: { name: '未定义', id: this.minus, image: 's' } };
        this.minus -= 1;
        if (this.currentnode.children !== undefined) {
          this.currentnode.children.push(ele);
        } else {
          // eslint-disable-next-line no-param-reassign
          this.currentnode.children = [];
          this.currentnode.children.push(ele);
        }
        console.log('addChildren');
      } else if (type === 'Honey') {
        const ele = { name: '未定义', id: this.minus, image: 's' };
        this.minus -= 1;
        if (this.currentnode.firstPerson !== undefined && this.currentnode.secondPerson === undefined) { // 说明只有左节点
          this.currentnode.secondPerson = ele;
          this.testnum += 1;
        } else if (this.currentnode.firstPerson === undefined && this.currentnode.secondPerson !== undefined) { // 说明只有右节点
          this.currentnode.firstPerson = ele;
        } else { // 说明两个节点都有
          this.$message({
            type: 'warning',
            message: '无法添加配偶',
          });
        }
        console.log('addHoney');
      } else if (type === 'Delete') {
        if (item.root === true) {
          this.$message({
            type: 'warning',
            message: '根元素无法删除！',
          });
        } else {
          // eslint-disable-next-line no-unused-vars
          this.test(this.currentchildren, item.id, 'Delete');
          // const ttemp = [];
          // ttemp.push(this.currentchildren);
          // ttemp.splice(0, 1);
          // delete this.currentchildren;
          // eslint-disable-next-line no-plusplus
          for (let i = 0; i < this.uppertree.length; ++i) {
            if (this.uppertree[i].firstPerson !== undefined && this.uppertree[i].firstPerson.id === item.id) {
              this.uppertree.splice(i, 1);
            } else if (this.uppertree[i].secondPerson !== undefined && this.uppertree[i].secondPerson.id === item.id) {
              this.uppertree.splice(i, 1);
            }
          }
        }
      } else {
        console.log('Error');
      }
    },
    // 递归遍历所有节点，根据id找到对应的children数组和节点
    test(tree, id, type) {
      this.$forceUpdate();
      let e;
      this.temptree = tree;
      // eslint-disable-next-line guard-for-in,no-restricted-syntax
      for (e of this.temptree) {
        if (type === 'Delete') {
          if (e.firstPerson !== undefined) {
            this.usedtable.splice(this.usedtable.indexOf(e.firstPerson.id), 1);
          }
          if (e.secondPerson !== undefined) {
            this.usedtable.splice(this.usedtable.indexOf(e.secondPerson.id), 1);
          }
          // eslint-disable-next-line no-restricted-syntax
          for (const user of this.userlist) {
            if (e.firstPerson !== undefined && user.id === e.firstPerson.id) {
              user.used = false;
            }
            if (e.secondPerson !== undefined && user.id === e.secondPerson.id) {
              user.used = false;
            }
          }
        }
        if (e.firstPerson !== undefined && e.firstPerson.id === id) {
          this.currentnode = e;// 当前节点，字典类型
          this.currentchildren = this.temptree; // 当前层，数组类型
          this.uppertree = this.temptree;
        }
        if (e.secondPerson !== undefined && e.secondPerson.id === id) {
          this.currentnode = e; // 当前节点，字典类型
          this.currentchildren = this.temptree; // 当前层，数组类型
          this.uppertree = this.temptree; // 总是返回上一层children数组
        }
        if (e.children !== undefined) { // 若它不是叶子结点
          if (type === 'Delete') {
            this.test(e.children, id, 'Delete');
          } else {
            this.test(e.children, id);
          } // 递归至下一个孩子层
        }
      }
    },
    clearGenealogy() {
      this.tree = [{
        firstPerson: {
          name: '未定义',
          image: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
          id: -1,
          defined: false,
          used: false,
          root: true,
        },
      }];
      // eslint-disable-next-line no-restricted-syntax
      for (const user of this.userlist) {
        user.used = false;
      }
      this.usedtable = [];
      this.minus = -2;
    },
    saveGenealogy() {
      const temp = {};
      temp.tree = this.tree;
      temp.usedtable = this.usedtable;
      temp.minus = this.minus;
      axios.post('/api/save-genealogy', { group_id: this.$props.info.id, content: temp })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            console.log(res.data.message);
          }
          this.$message({
            type: 'info',
            message: '家谱保存成功',
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    loadGenealogy() {
      axios.post('/api/query-genealogy', { group_id: this.$props.info.id })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            console.log(res.data.message);
            this.tree = res.data.content.tree;
            this.usedtable = res.data.content.usedtable;
            this.minus = res.data.content.minus;
          }
        })
        .catch((err) => {
          console.log(err);
        });
      this.loading = true;
      axios.post('/api/query-user', { group_id: this.$props.info.id })
        .then((res) => {
          this.loading = false;
          if (res.data.status) {
            this.$data.userlist = res.data.user_list;
            // eslint-disable-next-line no-restricted-syntax
            for (const user of this.userlist) { // 判断用户有没有已被家谱用过
              // eslint-disable-next-line no-restricted-syntax
              for (const id of this.usedtable) {
                if (id === user.id) {
                  user.used = true;
                  break;
                } else { user.used = false; }
              }
            }
            console.log(this.userlist);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    outputUsedtable() {
      console.log(this.usedtable);
      console.log(this.userlist);
      console.log(this.tree);
      console.log(this.currentnode);
      console.log(this.currentchildren);
      console.log(this.uppertree);
    },
    customizeName() {
      let q = false;
      // eslint-disable-next-line no-constant-condition,no-plusplus
      for (let i = 0; i > 1; --i) {
        this.randomnum = Math.round(Math.random() * 100000);
        console.log(this.randomnum);
        // eslint-disable-next-line no-restricted-syntax,no-plusplus
        for (let j = 0; j < this.userlist; ++j) {
          if (j === this.userlist.length - 1 && this.randomnum !== this.userlist[j].id) {
            q = true;
          }
        }
        if (q === true) {
          break;
        }
      }
    },
  },
  created() {
    this.loadGenealogy();
  },
};
</script>
<style lang="scss" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
}
.text-center {
  text-align: center;
  margin-bottom: 16px;
}
.custom-card {
  display: flex;
  align-items: center;
  width: 110px;
  padding: 5px;
  border: 0.5px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  background-color: #fff;
  cursor: pointer;
  box-shadow: 0 0 3px 1px rgba(#000, 0);
  transition: box-shadow .2s ease;
  &:hover {
    box-shadow: 0 0 3px 1px rgba(#000, .1);
  }
  &__image {
    flex: 0 0 auto;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #dedede;
    background-size: cover;
    background-position: 50%;
  }
  &__info {
    padding-left: 8px;
  }
  &__name {
    font-weight: 300;
  }
  &__age {
    margin-top: 2px;
    font-size: 6px;
  }
}
</style>
