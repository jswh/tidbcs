import axios from 'axios'
const HOST = 'http://127.0.0.1:5000'
async function executor(type: string, value: string) {
  let res = await axios.post(
    HOST + '/executor', {type, value}
  )
  return res
}
async function binaries() {
  let res = await axios.get(
    HOST + '/bins'
  )
  return res
}
async function executorState() {
  let res = await axios.get(
    HOST + '/executor'
  )
  return res
}

export default {
  HOST,
  executor,
  binaries,
  executorState
}
