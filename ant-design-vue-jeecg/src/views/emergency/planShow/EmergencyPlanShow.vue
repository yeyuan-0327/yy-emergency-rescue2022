<template>
  <div style="min-height: 800px;">
    <a-row>
      <a-col :span="5">
          <a-card style="min-height: 800px;margin-top: 1px" :bordered="false">
            <h3 style="margin-left: -15px;margin-top: -5px">
              规划方案
            </h3>
            <a-list item-layout="horizontal"
                    :data-source="planning_data">
              <a-list-item slot="renderItem" slot-scope="item, index">
                <a @click="showPlanning(item)" slot="actions">查看</a>
                <a @click="deletePlanning(item)" slot="actions">删除</a>
                <a-list-item-meta>
                  <span slot="title" >{{ item.planning_name }}</span>
                </a-list-item-meta>
              </a-list-item>
            </a-list>
          </a-card>
      </a-col>
      <a-col :span="19">
<!--        <a-card style="min-height: 800px" >-->
<!--          <div style="text-align: center;margin-top: 30%" >-->
<!--            <p>-->
<!--              点击左侧查看&#45;&#45;加载规划方案可视化结果-->
<!--            </p>-->
<!--            <p>-->
<!--              查看&#45;&#45;查看已得规划方案；删除&#45;&#45;删除无效规划方案-->
<!--            </p>-->
<!--          </div>-->
<!--        </a-card>-->
        <div style="background-color: #0B0F34;">
          <div class="headers" style="min-height: 800px;width: 1150px">
            <h1 class="header-title">3救援点-6险情规划可视化</h1>
            <div class="wrapper">
              <div class="content">
                <div class="col col-l">
                  <div class="xpanel-wrapper xpanel-wrapper-40">
                    <div class="xpanel xpanel-l-t">
                      <div class="title">
                        险情进展
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情1</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[0]" strokeColor="red" status="active"/>
                          </a-col>
                        </a-row>
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情2</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[1]" status="active"/>
                          </a-col>
                        </a-row>
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情3</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[2]" strokeColor="orange"  status="active"/>
                          </a-col>
                        </a-row>
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情4</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[3]" strokeColor="orange" status="active" />
                          </a-col>
                        </a-row>
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情5</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[4]" strokeColor="red" />
                          </a-col>
                        </a-row>
                      </div>
                      <div style="margin-top: 10px;padding-left: 20px">
                        <a-row>
                          <a-col :span="4">
                            <span style="color: white;">险情6</span>
                          </a-col>
                          <a-col :span="20">
                            <a-progress :percent="emergency_percent[5]" />
                          </a-col>
                        </a-row>
                      </div>
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-60">
                    <div class="xpanel xpanel-l-b">
                      <div class="title">
                        信息通报
                      </div>
                      <div class="marquee">
                        <div class="marquee_box" ref="marquee_box">
                          <ul class="marquee_list" :class="{marquee_top:animate}">
                            <p v-for="(item,index) in list" :key="index">
                              {{item}}
                            </p>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col col-c">
                  <div class="xpanel-wrapper xpanel-wrapper-75">
                    <div class="xpanel no-bg" id="flyChart" style="width: 100%;">
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-25">
                    <div class="xpanel xpanel-c-b">
                      <div class="title title-long">
                        规划方案
                      </div>
                      <h1 style="color:white;margin-top:20px;padding-left: 20px">救援点A:险情4、险情9</h1>
                      <h1 style="color:white;margin-top:10px;padding-left: 20px">救援点B:险情2、险情6</h1>
                      <h1 style="color:white;margin-top:10px;padding-left: 20px">救援点C:险情1、险情3、险情5、险情7、险情8</h1>

                    </div>
                  </div>
                </div>
                <div class="col col-r">
                  <div class="xpanel-wrapper xpanel-wrapper-25">
                    <div class="xpanel xpanel-r-t">
                      <div class="title">北京时间</div>
                        <span id="time"></span>
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-30">
                    <div class="xpanel xpanel-r-m" id="barChartMap">
                    </div>
                  </div>
                  <div class="xpanel-wrapper xpanel-wrapper-45">
                    <div class="xpanel xpanel-r-b" id="DashboardChart">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </a-col>
    </a-row>
  </div>

</template>

<script>
  import ACol from 'ant-design-vue/es/grid/Col'
  require('@/views/emergency/planShow/css/app.css')
  import * as echarts from 'echarts';
  import '@/views/emergency/planShow/js/echarts-map-china.js';

  const planning_data = [
    {
      plan_id:'1',
      planning_name: '3救援点-6险情',
    },
    {
      plan_id:'2',
      planning_name: '4救援点-12险情',
    },
    {
      plan_id:'3',
      planning_name: '100救援点-300险情',
    },
  ];
  const lunbo_list = [
    '某地发生4.6级地震，救援任务通报如下',
    '社会动员任务:集结进度20人',
    '紧急运输任务:某某运输完毕',
    '专业队伍任务:抢险队伍已到达',
    '医疗救助任务:医生某某已到达',
    '专业人才任务:高级工程师某某已到达',
    '生活保障任务:饮用水到达200箱',
    '人员搜救任务:搜救队伍A到达搜救点',
    '治安维护任务:治安维护民兵50人',
    '发生化学品泄漏事故致两人死亡，救援任务通报如下',
    '社会动员任务:志愿者集结30人',
    '医疗救助任务:医生护士到达50人',
    '专业人才任务:工程师集结20人',
    '人员防护任务:已庇护2000人',
    '卫生保障任务:医疗资源口罩完备',

  ];
  const emergency_percentList = [10,50,40,30,20,100];
  export default {
    name: 'EmergencyPlanShow',
    components: { ACol },
    data () {
      return {
        // plan
        selectedPlanningId:'',
        planning_data,
        // 轮播设置
        animate: false,
        showNum: 4,
        list:lunbo_list,
        //进度条
        emergency_percent:emergency_percentList,

      }
    },
    created () {
      // 轮播图页面显示
      setInterval(this.showMarquee, 2000)
      //时间大屏
      setInterval(this.time,1000);
      // process
      // setInterval(this.processAdd, 1000);
    },
    mounted () {
      this.$nextTick(_ => {
        this.flyMap()
        this.dashboardChartMap()
        this.barChartMap()
      })
      // 可见数据高度
      this.$refs.marquee_box.style.height = this.showNum * 100 + 'px'
      // 进度条定时器
    },
    methods: {
      //进度条
      processAdd(){
        for (let i  =0 ;i<emergency_percentList.length;i++){
          let percent = this.emergency_percent[i] + Math.random()*10;
          if (percent > 100) {
            percent = 0;
          }
          this.emergency_percent[i] = percent;
        }
      },
      //飞线图
      flyMap() {
        //初始化echarts实例
        const flyMap = echarts.init(document.getElementById("flyChart"));
        //城市经纬度
        const originName = '洛阳';
        const flyGeo = {
          '洛阳': [112.460299, 34.62677],
          '西安': [108.946466, 34.347269],
          '兰州': [103.84044, 36.067321],
          '乌鲁木齐': [87.62444, 43.830763],
          '包头': [109.846544, 40.662929],
          '西宁': [101.78443, 36.623393],
          '银川': [106.258602, 38.487834],
          '成都': [104.081534, 30.655822],
          '重庆': [106.558434, 29.568996],
          '拉萨': [91.120789, 29.65005],
          '昆明': [102.852448, 24.873998],
          '贵阳': [106.636577, 26.653325],
          '太原': [112.534919, 37.873219],
          '武汉': [114.311582, 30.598467],
          '长沙': [112.945473, 28.234889],
          '南昌': [115.864589, 28.689455],
          '合肥': [117.233443, 31.826578],
          '杭州': [120.215503, 30.253087],
          '广州': [113.271431, 23.135336],
          '北京': [116.413384, 39.910925],
          '天津': [117.209523, 39.093668]
        };
        //飞线数据
        let flyVal = [
          [{name: '洛阳'}, {name: '洛阳', value: 100}],
          [{name: '兰州'}, {name: '西安', value: 35}],
          [{name: '洛阳'}, {name: '兰州', value: 25}],
          [{name: '洛阳'}, {name: '乌鲁木齐', value: 55}],
          [{name: '洛阳'}, {name: '包头', value: 60}],
          [{name: '乌鲁木齐'}, {name: '西宁', value: 45}],
          [{name: '洛阳'}, {name: '银川', value: 35}],
          [{name: '洛阳'}, {name: '成都', value: 35}],
          [{name: '重庆'}, {name: '重庆', value: 40}],
          [{name: '洛阳'}, {name: '拉萨', value: 45}],
          [{name: '洛阳'}, {name: '昆明', value: 50}],
          [{name: '洛阳'}, {name: '贵阳', value: 55}],
          [{name: '洛阳'}, {name: '太原', value: 60}],
          [{name: '洛阳'}, {name: '武汉', value: 65}],
          [{name: '武汉'}, {name: '长沙', value: 70}],
          [{name: '杭州'}, {name: '南昌', value: 75}],
          [{name: '洛阳'}, {name: '合肥', value: 80}],
          [{name: '洛阳'}, {name: '杭州', value: 85}],
          [{name: '北京'}, {name: '广州', value: 90}],
          [{name: '洛阳'}, {name: '北京', value: 95}],
          [{name: '洛阳'}, {name: '天津', value: 60}],
        ];
        //数据转换，转换后格式：[{fromName:'cityName', toName:'cityName', coords:[[lng, lat], [lng, lat]]}, {...}]
        const convertFlyData = function(data) {
          let res = [];
          for(let i=0;i<data.length;i++) {
            let dataItem = data[i];
            let toCoord = flyGeo[dataItem[0].name];
            let fromCoord = flyGeo[dataItem[1].name];
            if(fromCoord && toCoord) {
              res.push({
                fromName: dataItem[1].name,
                toName: dataItem[0].name,
                coords: [fromCoord, toCoord]
              });
            }
          }
          return res;
        };
        //报表配置
        const flySeries = [];
        [[originName, flyVal]].forEach(function(item, i) {
          console.log("item is " , item);
          flySeries.push({
            name: item[0],
            type: 'lines',
            zlevel: 1,
            symbol: ['none', 'none'],
            symbolSize: 0,
            effect: { //特效线配置
              show: true,
              period: 5, //特效动画时间，单位s
              trailLength: 0.1, //特效尾迹的长度，从0到1
              symbol: 'arrow',
              symbolSize: 5
            },
            lineStyle: {
              normal: {
                color: '#f19000',
                width: 1,
                opacity: 0.6,
                curveness: 0.2 //线的平滑度
              }
            },
            data: convertFlyData(item[1])
          }, {
            name: item[0],
            type: 'effectScatter',
            coordinateSystem: 'geo',
            zlevel: 2,
            rippleEffect: { //涟漪特效
              period: 5, //特效动画时长
              scale: 4, //波纹的最大缩放比例
              brushType: 'stroke' //波纹的绘制方式：stroke | fill
            },
            label: {
              normal: {
                show: false,
                position: 'right',
                formatter: '{b}'
              }
            },
            symbol: 'circle',
            symbolSize: function (val) {
              //根据某项数据值设置符号大小
              return val[2] / 10;
            },
            itemStyle: {
              normal: {
                color: '#f19000'
              }
            },
            data: item[1].map(function(dataItem) {
              return {
                name: dataItem[1].name,
                value: flyGeo[dataItem[1].name].concat([dataItem[1].value])
              };
            })
          }, { //与上层的点叠加
            name: item[0],
            type: 'scatter',
            coordinateSystem: 'geo',
            zlevel: 3,
            symbol: 'circle',
            symbolSize: function (val) {
              //根据某项数据值设置符号大小
              return val[2] / 15;
            },
            itemStyle: {
              normal: {
                color: '#f00'
              }
            },
            data: item[1].map(function(dataItem) {
              return {
                name: dataItem[1].name,
                value: flyGeo[dataItem[1].name].concat([dataItem[1].value])
              };
            })
          });
        });

        //报表配置项
        const flyMapOpt = {
          title: {
            show: true,
            text: '实时动态图',
            x: 'center',
            y:'50px',
            textStyle: {
              color: '#fff',
              fontWeight:'normal',
              fontSize:21
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              if(params.value) {
                return params.name + ' : ' + params.value[2];
              }else {
                return params.name;
              }
            }
          },
          geo: {
            map: 'china',
            zoom: 1.2,
            label: {
              normal: {
                show: false,
                textStyle: {
                  color: '#FFFFFF',
                },
              },
              emphasis: {
                show: false,
              },
            },
            roam: true, //是否允许缩放
            itemStyle: {
              normal: {
                color: '#101f32', //地图背景色
                borderColor: '#22ccfb', //省市边界线00fcff 516a89
                borderWidth: 1,
                textStyle: '#fff',
              },
              emphasis: {
                color: '#22ccfb', //悬浮背景
              },
            },
            data: [],
          },
          series: flySeries
        };

        //渲染报表
        flyMap.setOption(flyMapOpt);
      },
      // 仪表图
      dashboardChartMap(){
        const dashboardMap = echarts.init(document.getElementById("DashboardChart"));
        let option;
        const gaugeData = [
          {
            value: 0,
            name: '志愿者',
            title: {
              offsetCenter: ['-40%', '80%']
            },
            detail: {
              offsetCenter: ['-40%', '95%']
            }
          },
          {
            value: 0,
            name: '救援车辆',
            title: {
              offsetCenter: ['0%', '80%']
            },
            detail: {
              offsetCenter: ['0%', '95%']
            }
          },
          {
            value: 0,
            name: '人防队伍',
            title: {
              offsetCenter: ['40%', '80%']
            },
            detail: {
              offsetCenter: ['40%', '95%']
            }
          }
        ];
        option = {
          title: {
            x:'left',
            text: '调度情况',
            textStyle: {
              color: '#FFFFFF',
              fontSize:21,
              fontWeight:'normal'
            },
          },
          series: [
            {
              type: 'gauge',
              radius:'80%',
              anchor: {
                show: true,
                showAbove: true,
                size: 15,
                itemStyle: {
                  color: '#FAC858'
                }
              },
              pointer: {
                icon: 'path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z',
                width: 8,
                length: '80%',
                offsetCenter: [0, '8%']
              },
              progress: {
                show: true,
                overlap: true,
                roundCap: true
              },
              axisLine: {
                roundCap: true
              },
              data: gaugeData,
              title: {
                fontSize: 12,
                color: '#fff',
              },
              detail: {
                width: 20,
                height: 10,
                fontSize: 12,
                color: '#fff',
                backgroundColor: 'auto',
                borderRadius: 3,
                formatter: '{value}%'
              }
            }
          ]
        };
        setInterval(function () {
          if (gaugeData[0].value > 100) gaugeData[0].value = 0;
          else gaugeData[0].value += Math.round(Math.random()*10);
          if (gaugeData[1].value > 100) gaugeData[1].value = 0;
          else gaugeData[1].value += Math.round(Math.random()*10);
          if (gaugeData[2].value > 100) gaugeData[2].value = 0;
          else gaugeData[2].value += Math.round(Math.random()*10);
          dashboardMap.setOption({
            series: [
              {
                data: gaugeData
              }
            ]
          });
        }, 2000);

        dashboardMap.setOption(option);
      },
      // bar
      barChartMap(){
        const barChartMap = echarts.init(document.getElementById("barChartMap"));
        let option = {
          grid:{
            height:120
          },
          title: {
            x:'left',
            text: '应急资源需求',
            textStyle: {
              color: '#FFFFFF',
              fontSize:21,
              fontWeight:'normal'
            },
          },
          tooltip: {},
          dataset: {
            source: [
              ['product', '需志愿者', '需救援车辆', '需人防队伍'],
              ['险情1', 20, 2, 2],
              ['险情2', 20, 13, 2],
              ['险情3', 40, 2, 6],
              ['险情4', 10, 6, 6],
              ['险情5', 10, 27, 1],
              ['险情6', 50, 4, 4]
            ]
          },
          xAxis: {
            axisLabel:{
              rotate:10,
              interval:0,
              textStyle: {
                show:true,
                color: "#fff",
                fontSize: 10,
              },
            },
            type: 'category'
          },
          yAxis: {
            axisLabel:{
              textStyle: {
                show:true,
                color: '#fff',
                fontSize: 10,
              },
            },
          },
          // Declare several bar series, each will be mapped
          // to a column of dataset.source by default.
          series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
        };

        barChartMap.setOption(option);
      },
      //按钮效果
      showPlanning(item){
        this.selectedPlanningId = item.plan_id
        console.log(item)
      },
      deletePlanning(){
      },
      // 轮播图
      showMarquee () {
        this.animate = true
        this.list.push(this.list[0])
        setTimeout(() => {
          this.list.shift()
          this.animate = false
        }, 2000)
      },
      //时间函数
      time(){
        //顶部时间
        const myDate = new Date();
        const myYear = myDate.getFullYear(); //获取完整的年份(4位,1970-????)
        const myMonth = myDate.getMonth()+1; //获取当前月份(0-11,0代表1月)
        const myToday = myDate.getDate(); //获取当前日(1-31)
        const myDay = myDate.getDay(); //获取当前星期X(0-6,0代表星期天)
        const myHour = myDate.getHours(); //获取当前小时数(0-23)
        const myMinute = myDate.getMinutes(); //获取当前分钟数(0-59)
        const mySecond = myDate.getSeconds(); //获取当前秒数(0-59)
        const week = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
        let nowTime;
        nowTime = myYear+'年'+fillZero(myMonth)+'月'+fillZero(myToday)+'日'+'<br>'
          +'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'+week[myDay]+'：'+
          fillZero(myHour)+':'+ fillZero(myMinute)+':'+fillZero(mySecond)+'<br>'
          +'&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp已耗时：1小时' + (myMinute+6) +'分'+mySecond+'秒';
        document.getElementById("time").innerHTML = nowTime
        function fillZero(str){
          let realNum;
          if(str<10){
            realNum	= '0'+str;
          }else{
            realNum	= str;
          }
          return realNum;
        }
      }
    },
  }
</script>

<style scoped >
  .headers {position:relative;height:42px;box-sizing:border-box;}
  .marquee {
    width: 90%;
    margin-left: 10px;
    align-items: center;
    color: white;
    background-color: #0b0f34;
    display: flex;
    box-sizing: border-box;
    overflow: hidden;
  }
  .marquee_title {
    padding: 0 20px;
    height: 21px;
    font-size: 14px;
    border-right: 1px solid #d8d8d8;
    align-items: center;
  }
  .marquee_box {
    display: block;
    position: relative;
    width: 90%;
    overflow: hidden;
    margin: 0 auto;
  }
  .marquee_list {
    display: block;
    position: absolute;
    top: 0px;
    left: -40px;
  }
  .marquee_top {
    transition: all 1s;
    margin-top: -30px;
  }
  .marquee_list li {
    height: 30px;
    line-height: 30px;
    font-size: 14px;
    padding-left: 20px;
  }
  .marquee_list li span {
    padding: 0 2px;
  }
  #time{
    width: 100%;
    padding-left: 20px;
    font-size: 20px;
    text-align: center;
    color: #ffffff;
    line-height: 50px;
    margin-right: 20px;
  }
</style>