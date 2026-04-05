import config from 'src/config';
import { EMAIL_TEMPLATE } from 'src/utils/resend';

/**
 * 이메일 인증
 * 주어진 locale과 token을 기반으로 이메일 인증 메일의 제목과 내용을 생성합니다.
 * @param locale 사용자 언어 설정 (예: "ko" 또는 "en")
 * @param token 인증을 위한 토큰
 * @returns 이메일 인증 메일의 제목(subject)과 내용(content)을 포함하는 객체
 */
export const createEmailVerificationContent = (
  locale: string,
  token: string,
) => ({
  subject: locale === 'ko' ? '이메일 인증 메일' : 'Email Verification Mail',
  content: EMAIL_TEMPLATE(
    locale === 'ko' ? '이메일 인증 메일' : 'Email Verification Mail',
    locale === 'ko'
      ? '아래 버튼을 클릭하여 인증을 완료해주세요.'
      : 'Click the button below to verify your email.',
    locale === 'ko' ? '확인하기' : 'Check it out',
    // 인증 링크 생성
    `${config.webEndpoint}/${locale}/verify?token=${token}`,
  ),
});

/**
 * 비밀번호 재설정
 * 주어진 locale과 token을 기반으로 비밀번호 재설정 메일의 제목과 내용을 생성합니다.
 * @param locale 사용자 언어 설정 (예: "ko" 또는 "en")
 * @param token 재설정을 위한 토큰
 * @returns 비밀번호 재설정 메일의 제목(subject)과 내용(content)을 포함하는 객체
 */
export const createPasswordResetContent = (token: string) => {
  const title = '비밀번호 재설정 안내';
  const content = '아래 버튼을 클릭하여 비밀번호를 재설정해주세요.';

  const buttonText = '비밀번호 재설정';
  const buttonLink = `${config.webEndpoint}/reset-password?token=${token}`;

  return {
    subject: title,
    content: EMAIL_TEMPLATE(title, content, buttonText, buttonLink),
  };
};
