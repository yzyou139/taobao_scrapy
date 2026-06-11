/**
 * 淘宝 mtop 接口签名生成器
 * 用法:
 *   const sign = require('./mtop_sign');
 *   // 生成 sign
 *   const result = sign.generate(TOKEN, APP_KEY, { itemId: "...", page: 1, ... });
 *   console.log(result.sign);
 *
 * 命令行调用 (Windows PowerShell 用双引号，内部双引号转义):
 *   node mtop_sign.js <token> <appKey> "<data_json>"
 *   node mtop_sign.js "048c99c37a276e3297c90655e66cf6e1" "12574478" "{\"itemId\":\"865028697626\",\"page\":1}"
 */

const crypto = require('crypto');

/**
 * 生成淘宝 mtop 接口签名
 * @param {string} token - 从 _m_h5_tk cookie 提取的令牌（_ 前面部分）
 * @param {string} appKey - 应用标识，默认 "12574478"
 * @param {object|string} data - 请求体数据（对象或 JSON 字符串）
 * @returns {{ t: string, data: string, sign: string }}
 */
function generate(token, appKey = '12574478', data = {}) {
  // 1. 当前时间戳（毫秒）
  const t = String(Date.now());

  // 2. data 序列化为紧凑 JSON（去掉 : 和 , 后面的空格，与淘宝页面一致）
  const dataStr = typeof data === 'string'
    ? data
    : JSON.stringify(data).replace(/, /g, ',').replace(/: /g, ':');

  // 3. 拼接原始字符串
  const raw = token + '&' + t + '&' + appKey + '&' + dataStr;

  // 4. MD5 签名
  const sign = crypto.createHash('md5').update(raw, 'utf8').digest('hex');

  return { t, data: dataStr, sign };
}

// ========== 直接运行测试（无参数时） ==========
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    // 无参数 → 运行内置测试
    const token = '048c99c37a276e3297c90655e66cf6e1';
    const appKey = '12574478';
    const data = {
      itemId: '865028697626',
      userId: 2212201318745,
      pageSize: 10,
      page: 1,
      type: 'mix_group',
      tagId: '',
      ecode: 0,
      biz: 'pc'
    };
    const result = generate(token, appKey, data);
    console.log('sign:', result.sign);
    console.log('t:   ', result.t);
    console.log('data:', result.data);
  } else {
    // 有参数 → 命令行模式
    const token = args[0];
    const appKey = args[1] || '12574478';
    let data = args[2] || '{}';
    try { data = JSON.parse(data); } catch (e) { /* 保持字符串 */ }

    const result = generate(token, appKey, data);
    console.log(JSON.stringify({
      t: result.t,
      data: result.data,
      sign: result.sign,
      raw: token + '&' + result.t + '&' + appKey + '&' + result.data
    }, null, 2));
  }
}

module.exports = { generate };

console.log(generate('048c99c37a276e3297c90655e66cf6e1', '12574478', { itemId: '865028697626', page: 1 }).sign);