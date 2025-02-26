import { nunitoBold, nunitoSemiBold } from "../_font-config/nunito-google-font";
import Link from "next/link";
import SimpleNavBar from "./SimpleNavBar";

export default function HeroHeader() {
  return (
    <section className={`hero`}>
      <div className="hero-body is-flex is-vcentered is-justify-content-space-between">
        <div>
          <h1 className={`mb-2 my-title title is-2 ${nunitoBold.className}`}>
            <Link href={`${process.env.MAIN_SITE_BASE_URL}`}>
              Patrick Meaney
            </Link>
          </h1>
          <h2 className={`subtitle is-4 ${nunitoSemiBold.className}`}>
            Web App, Cloud, DevOps Engineer
          </h2>
        </div>
        <SimpleNavBar />
      </div>
    </section>
  );
}
