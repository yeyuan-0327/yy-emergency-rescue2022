<template>
  <a-card :bordered="false">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="表名">
              <a-input placeholder="请输入表名" v-model="queryParam.name"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchReset" icon="reload" style="margin-left: 8px">重置</a-button>
<!--              <a @click="handleToggleSearch" style="margin-left: 8px">-->
<!--                {{ toggleSearchStatus ? '收起' : '展开' }}-->
<!--                <a-icon :type="toggleSearchStatus ? 'up' : 'down'"/>-->
<!--              </a>-->
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->

    <!-- 操作按钮区域 -->
    <div class="table-operator">
      <a-button @click="handleAdd" type="primary" icon="plus">新增</a-button>
      <a-button type="primary" icon="download" @click="handleExportXls('基础数据库信息表')">导出</a-button>
<!--      <a-upload name="file" :showUploadList="false" :multiple="false" :headers="tokenHeader" :action="importExcelUrl" @change="handleImportExcel">-->
<!--        <a-button type="primary" icon="import">导入</a-button>-->
<!--      </a-upload>-->
      <!-- 高级查询区域 -->
<!--      <j-super-query :fieldList="superFieldList" ref="superQueryModal" @handleSuperQuery="handleSuperQuery"></j-super-query>-->
      <a-dropdown v-if="selectedRowKeys.length > 0">
        <a-menu slot="overlay">
          <a-menu-item key="1" @click="batchDel"><a-icon type="delete"/>删除</a-menu-item>
        </a-menu>
        <a-button style="margin-left: 8px"> 批量操作 <a-icon type="down" /></a-button>
      </a-dropdown>
    </div>

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
        rowKey="id"
        :columns="columns"
        :dataSource="dataSource"
        :pagination="ipagination"
        :loading="loading"
        :rowSelection="{selectedRowKeys: selectedRowKeys, onChange: onSelectChange}"
        class="j-table-force-nowrap"
        @change="handleTableChange">

        <template slot="htmlSlot" slot-scope="text">
          <div v-html="text"></div>
        </template>
        <template slot="imgSlot" slot-scope="text">
          <span v-if="!text" style="font-size: 12px;font-style: italic;">无图片</span>
          <img v-else :src="getImgView(text)" height="25px" alt="" style="max-width:80px;font-size: 12px;font-style: italic;"/>
        </template>
        <template slot="fileSlot" slot-scope="text">
          <span v-if="!text" style="font-size: 12px;font-style: italic;">无文件</span>
          <a-button
            v-else
            :ghost="true"
            type="primary"
            icon="download"
            size="small"
            @click="downloadFile(text)">
            下载
          </a-button>
        </template>

        <span slot="action" slot-scope="text, record">
          <a @click="handleEdit(record)">编辑</a>

          <a-divider type="vertical" />
          <a-dropdown>
            <a class="ant-dropdown-link">更多 <a-icon type="down" /></a>
            <a-menu slot="overlay">
              <a-menu-item>
                <a @click="clickDatabaseToShow(record)">详情</a>
              </a-menu-item>
              <a-menu-item>
                <a-popconfirm title="确定删除吗?" @confirm="() => handleDelete(record.id)">
                  <a>删除</a>
                </a-popconfirm>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </span>

      </a-table>
    </div>
    <a-modal v-model="showDatabaseVisible"
             :title="showDatabaseVisibleTitle"
             switchFullscreen
             :width="1400"
             :okButtonProps="{class:{'jee-hidden': true} }"
             cancelText="关闭">

      <a-table v-show="showType === 'table'"
               bordered
               :scroll="{ x: 300, y: 300 }"
               :columns="showDatabaseTableColumns"
               :dataSource="showDatabaseSource"
               :loading="showDatabaseTableLoading">
        <!--        :pagination="paginationDatabaseOpt"-->
      </a-table>

      <div v-show="showType === 'chart'" >
        <a-row :gutter="16">
          <a-col :span="12">
            <a-card :bordered="true" style="height: 250px">
              <div id="databaseColumnChart" :style="{width: '650px', height: '250px'}">
              </div>
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card :bordered="true" style="height: 250px">
            </a-card>
          </a-col>
        </a-row>
        <br/>
        <a-row>
          <a-col :span="24">
            <a-card :bordered="true" style="height: 300px">
            </a-card>
          </a-col>
        </a-row>
      </div>
      <br/>
      <a-radio-group v-model="showType">
        <a-radio-button value="table" @click="tableClick()">
          表
        </a-radio-button>
        <a-radio-button value="chart" @click="chartClick()">
          图
        </a-radio-button>
      </a-radio-group>

    </a-modal>
    <database-info-modal ref="modalForm" @ok="modalFormOk"></database-info-modal>
  </a-card>
</template>

<script>

  import '@/assets/less/TableExpand.less'
  import { mixinDevice } from '@/utils/mixin'
  import { JeecgListMixin } from '@/mixins/JeecgListMixin'
  import DatabaseInfoModal from './modules/DatabaseInfoModal'
  import {filterMultiDictText} from '@/components/dict/JDictSelectUtil'
  import ACol from 'ant-design-vue/es/grid/Col'
  import ARow from 'ant-design-vue/es/grid/Row'

  export default {
    name: 'DatabaseInfoList',
    mixins:[JeecgListMixin, mixinDevice],
    components: {
      ARow,
      ACol,
      DatabaseInfoModal,
    },
    data () {
      return {
        description: '基础数据库信息表管理页面',
        //弹出框
        showDatabaseVisibleTitle: '标题',
        showDatabaseVisible: false,
        showType: 'table',
        //选中的单一数据库详细信息 表
        showDatabaseTableColumns:[],
        showDatabaseSource:[],
        showDatabaseTableLoading:false,
        //选中的单一数据库详细信息 图
        // 数据库信息表头
        columns: [
          {
            title: '#',
            dataIndex: '',
            key:'rowIndex',
            width:60,
            align:"center",
            customRender:function (t,r,index) {
              return parseInt(index)+1;
            }
          },
          {
            title:'表名',
            align:"center",
            dataIndex: 'name'
          },
          {
            title:'中文名',
            align:"center",
            dataIndex: 'chineseName'
          },
          {
            title:'数据库类型',
            align:"center",
            dataIndex: 'databaseProject_dictText'
          },
          {
            title:'描述信息',
            align:"center",
            dataIndex: 'content'
          },
          {
            title:'创建日期',
            align:"center",
            dataIndex: 'createTime'
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
        url: {
          list: "/datamanage/databaseInfo/list",
          delete: "/datamanage/databaseInfo/delete",
          deleteBatch: "/datamanage/databaseInfo/deleteBatch",
          exportXlsUrl: "/datamanage/databaseInfo/exportXls",
          importExcelUrl: "datamanage/databaseInfo/importExcel",
        },
        dictOptions:{},
        superFieldList:[],
        //chart名称
        myDatabaseColumnChart:null
      }
    },
    created() {
      this.getSuperFieldList();
    },
    //chart加载函数
    // mounted(){
    //   this.$nextTick(()=>{
    //     this.initData()
    //   })
    // },
    computed: {
      importExcelUrl: function(){
        return `${window._CONFIG['domianURL']}/${this.url.importExcelUrl}`;
      },
    },
    methods: {
      initDictConfig(){
      },
      getSuperFieldList(){
        let fieldList=[];
        fieldList.push({type:'string',value:'name',text:'表名',dictCode:''})
        fieldList.push({type:'string',value:'chineseName',text:'中文名',dictCode:''})
        fieldList.push({type:'string',value:'databaseProject',text:'数据库类型',dictCode:'database_project'})
        fieldList.push({type:'string',value:'content',text:'描述信息',dictCode:''})
        fieldList.push({type:'datetime',value:'createTime',text:'创建日期'})
        this.superFieldList = fieldList
      },
      //chart初始化数据
      initData(){
        let option = {
          title: { text: '在Vue中使用echarts', textStyle: { fontSize: 15 } },
          tooltip: {},
          xAxis: {
            data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
          },
          yAxis: {},
          series: [{
            name: '销量',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }]
        };
        if(this.myDatabaseColumnChart == null) this.myDatabaseColumnChart = this.$echarts.init(document.getElementById('databaseColumnChart'))
        else this.myDatabaseColumnChart.clear()
        this.myDatabaseColumnChart.setOption(option,true)
      },
      //详情事件
      clickDatabaseToShow(record){
        this.showDatabaseVisible = true;
        console.log(record)
      },
      //弹出框 表图切换按钮点击事件
      tableClick(){
      },
      chartClick(){
        this.initData()
      },
    }
  }
</script>
<style scoped>
  @import '~@assets/less/common.less';
</style>