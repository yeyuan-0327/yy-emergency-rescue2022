package org.jeecg.modules.demo.databasemanage.service.impl;

import org.jeecg.modules.demo.databasemanage.entity.DatabaseInfo;
import org.jeecg.modules.demo.databasemanage.mapper.DatabaseInfoMapper;
import org.jeecg.modules.demo.databasemanage.service.IDatabaseInfoService;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

/**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-07-30
 * @Version: V1.0
 */
@Service
public class DatabaseInfoServiceImpl extends ServiceImpl<DatabaseInfoMapper, DatabaseInfo> implements IDatabaseInfoService {

}
