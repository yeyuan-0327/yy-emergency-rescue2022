<template>
  <a-card :bordered="false">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="规则名">
              <a-input placeholder="请输入规则名" v-model="searchRuleName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchRuleQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchRuleReset" icon="reload" style="margin-left: 8px">重置</a-button>
              <a-dropdown v-if="selectedRowKeys.length > 0">
                <a-menu slot="overlay">
                  <a-menu-item key="1" @click="batchSelectDel"><a-icon type="delete"/>删除</a-menu-item>
                </a-menu>
              <a-button style="margin-left: 8px"> 批量操作 <a-icon type="down" /></a-button>
            </a-dropdown>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->
    <!-- table区域-begin -->
    <div>
      <div class="ant-alert ant-alert-info" style="margin-bottom: 16px;">
        <i class="anticon anticon-info-circle ant-alert-icon"></i> 已选择 <a style="font-weight: 600">{{ selectedRowKeys.length }}</a>项
        <a style="margin-left: 24px" @click="onClearSelected">清空</a>
      </div>
      <a-table
        ref="table"
        size="middle"
        :scroll="{x:true}"
        bordered
        rowKey="rowKey"
        :columns="columns"
        :dataSource="dataSource"
        :pagination="paginationOpt"
        :loading="loading"
        :rowSelection="{selectedRowKeys: selectedRowKeys, onChange: onSelectChange}"
        class="j-table-force-nowrap">

        <span slot="action" slot-scope="text, record">
          <a @click="clickRuleToShow(record)">详情</a>
          <a-divider type="vertical" />
          <a-popconfirm title="确定删除吗?" @confirm="() => handleRuleDelete(record.rowKey)">
            <a>删除</a>
          </a-popconfirm>
        </span>

      </a-table>
    </div>

    <a-modal v-model="ruleWriteModal"
             :title="ruleWriteModalTitle"
             :confirm-loading="confirmLoading"
             switchFullscreen
             :width="1000"
             :okButtonProps="{class:{'jee-hidden': true} }"
             @cancel="ruleWriteCancel">
      <a-form-model
        a-form-model :label-col="labelCol" :wrapper-col="wrapperCol">
        <a-form-model-item label="规则名称" required>
        </a-form-model-item>
        <a-form-model-item label="所属险情" required>
        </a-form-model-item>
        <a-form-model-item label="失效时间" required >
        </a-form-model-item>
        <a-form-model-item label="规则类型" >
          <span v-show="ruleType==='Jar'">
            Jar类型
          </span>
          <span  v-show="ruleType==='Excel'">
            Excel类型
          </span>
          <span v-show="ruleType==='Drl'">
            Drl类型
          </span>
        </a-form-model-item>
        <a-form-model-item label="规则链接" >
        </a-form-model-item>
        <a-form-model-item label="规则详情" >
          {{ruleMeta}}
        </a-form-model-item>

      </a-form-model>
    </a-modal>

  </a-card>
</template>

<script>
  import '@/assets/less/TableExpand.less'

  const data = [];
  for (let i = 0; i < 46; i++) {
    data.push({
      rowKey: i,
      name: `Edward King ${i}`,
      age: 32,
      address: `London, Park Lane no. ${i}`,
    });
  }

  export default {
    name: 'RuleList',
    data () {
      return {
        //详情modal
        ruleWriteModal:false,
        ruleWriteModalTitle:"",
        confirmLoading: false,
        ruleType:"",

        //表格上方内容配置
        searchRuleName:"",
        selectedRowKeys:[],
        loading:false,
        //表格配置
        columns:[
          {
            title: 'Name',
            align:"center",
            dataIndex: 'name',
            filteredValue: this.searchRuleName ? this.searchRuleName: null,
          },
          {
            title: 'Age',
            align:"center",
            dataIndex: 'age',
          },
          {
            title: 'Address',
            align:"center",
            dataIndex: 'address',
          },
          {
            title: '操作',
            dataIndex: 'action',
            align:"center",
            fixed:"right",
            width:147,
            scopedSlots: { customRender: 'action' }
          }
        ],
        dataSource:data,
        //表格数据分页设置
        paginationOpt: {
          defaultCurrent: 1, // 默认当前页数
          defaultPageSize: 10, // 默认当前页显示数据的大小
          total: 0, // 总数，必须先有
          showSizeChanger: true,
          showQuickJumper: true,
          pageSizeOptions: ["5", "10", "15", "20"],
          showTotal: (total) => `共 ${total} 条`, // 显示总数
          onShowSizeChange: (current, pageSize) => {
            this.paginationOpt.defaultCurrent = 1;
            this.paginationOpt.defaultPageSize = pageSize;
          },
          // 改变每页数量时更新显示
          onChange: (current, size) => {
            this.paginationOpt.defaultCurrent = current;
            this.paginationOpt.defaultPageSize = size;
          },
        },

        //modal 内容
        labelCol: { span: 4 },
        wrapperCol: { span: 14 },
        ruleMeta: "123",

      }
    },
    methods:{
      //规则名搜索按钮
      searchRuleQuery(){
        console.log("搜索按钮")
        if (this.dataSource && this.searchRuleName !== '') {
          this.dataSource = this.dataSource.filter(
            (p) => p.name.indexOf(this.searchRuleName) !== -1
          )
        } else {
          this.dataSource=data
        }
      },
      //重置搜索按钮
      searchRuleReset(){
        this.searchRuleName = ''
        console.log("重置搜索按钮")
      },
      //清空已选择
      onClearSelected(){
        this.selectedRowKeys=[]
      },
      //选项改变的时候
      onSelectChange(selectedRowKeys){
        this.selectedRowKeys = selectedRowKeys;
      },
      //详情按钮
      clickRuleToShow(){
        this.ruleWriteModalTitle = "Jar接口"
        this.ruleType = 'Jar';
        this.ruleWriteModal = true
      },
      //详情关闭按钮
      ruleWriteCancel(){
      },
      //单个删除按钮
      handleRuleDelete(id){
        console.log(id)
      },
      //批量删除
      batchSelectDel(){
        console.log(this.selectedRowKeys)
      }
    }
  }
</script>

<style scoped>

</style>