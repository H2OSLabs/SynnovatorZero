import type { NextPageContext } from "next"

export default function ErrorPage({ statusCode }: { statusCode?: number }) {
  return (
    <div className="min-h-screen bg-nf-background text-nf-white flex items-center justify-center px-6">
      <div className="max-w-md w-full text-center">
        <h1 className="font-heading text-3xl font-bold mb-3">出错了</h1>
        <p className="text-nf-muted">
          {typeof statusCode === "number" ? `请求失败（HTTP ${statusCode}）` : "发生未知错误"}
        </p>
      </div>
    </div>
  )
}

ErrorPage.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res?.statusCode ?? err?.statusCode
  return { statusCode }
}
