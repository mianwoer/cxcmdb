import os

from sre_buff.utils.third_party.wechat_webhook.wechat_robot import send_markdown


def test_wechat_rebot(requests_mock):
    requests_mock.post(
        os.environ.get("WECHAT_ROBOT_ENDPOINT", ""),
        status_code=200,
        json={"errcode": 0},
    )
    res = send_markdown(
        dict(
            env="生产环境",
            product_line="智能汽车",
            role="产品",
            severity="critical",
            status="resloved",
            description="是的粉丝的方式都放啥地方",
            area="森华机房",
            url="https://in.iflytek.com",
        )
    )
    assert res
