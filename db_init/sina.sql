-- postgresql数据库
-- 新浪评论表
DROP TABLE IF EXISTS public.sina_comment;
CREATE TABLE public.sina_comment(
    comment_id character varying(20),
    user_name text,
    created_at text,
    comment text,
    like_counts text
);
COMMENT ON TABLE public.sina_comment IS '新浪评论详情';
COMMENT ON COLUMN public.sina_comment.comment_id IS '用户id';
COMMENT ON COLUMN public.sina_comment.user_name IS '用户名';
COMMENT ON COLUMN public.sina_comment.created_at IS '评论时间';
COMMENT ON COLUMN public.sina_comment.comment IS '评论内容';
COMMENT ON COLUMN public.sina_comment.like_counts IS '点赞数';
